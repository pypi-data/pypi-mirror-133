import hashlib
from functools import reduce
from typing import List, Tuple
from logging import Logger
from pyspark.sql import DataFrame
from pyspark.sql import functions as f
from pyspark.sql.window import Window
from featurestorebundle.entity.Entity import Entity
from featurestorebundle.feature.FeaturesStorage import FeaturesStorage
from featurestorebundle.delta.feature.DeltaRainbowTableManager import DeltaRainbowTableManager
from featurestorebundle.delta.EmptyDataFrameCreator import EmptyDataFrameCreator
from featurestorebundle.feature.reader.FeaturesReaderInterface import FeaturesReaderInterface
from featurestorebundle.delta.feature.schema import (
    get_feature_store_initial_schema,
    get_rainbow_table_schema,
    get_rainbow_table_hash_column,
    get_rainbow_table_features_column,
)


class FeaturesPreparer:
    def __init__(
        self,
        logger: Logger,
        join_type: str,
        join_batch_size: int,
        checkpoint_before_merge: bool,
        features_reader: FeaturesReaderInterface,
        rainbow_table_manager: DeltaRainbowTableManager,
        empty_dataframe_creator: EmptyDataFrameCreator,
    ):
        self.__logger = logger
        self.__join_type = join_type
        self.__join_batch_size = join_batch_size
        self.__checkpoint_before_merge = checkpoint_before_merge
        self.__features_reader = features_reader
        self.__rainbow_table_manager = rainbow_table_manager
        self.__empty_dataframe_creator = empty_dataframe_creator

    def prepare(self, features_storage: FeaturesStorage) -> Tuple[DataFrame, DataFrame]:
        entity = features_storage.entity
        feature_list = features_storage.feature_list

        base_dataframe = self.__prepare_base_dataframe(features_storage)

        if self.__checkpoint_before_merge:
            self.__logger.info("Checkpointing features data")

            base_dataframe = base_dataframe.checkpoint()

            self.__logger.info("Checkpointing done")

        features_data = base_dataframe.select(
            entity.id_column,
            entity.time_column,
            get_rainbow_table_hash_column().name,
            *feature_list.get_names(),
        )

        rainbow_data = base_dataframe.select(
            get_rainbow_table_hash_column().name,
            get_rainbow_table_features_column().name,
        ).distinct()

        return features_data, rainbow_data

    # pylint: disable=too-many-locals
    def __prepare_base_dataframe(self, features_storage: FeaturesStorage) -> DataFrame:
        if not features_storage.results:
            raise Exception("There are no features to write.")

        entity = features_storage.entity
        feature_list = features_storage.feature_list
        results = features_storage.results
        pk_columns = [entity.id_column, entity.time_column]
        technical_columns = pk_columns + [get_rainbow_table_hash_column().name]

        feature_store = self.__load_feature_store(entity)
        rainbow_table = self.__load_rainbow_table(entity)

        if self.__join_type == "left_with_checkpointing":
            join_method = self.__join_dataframes_using_left_join

        elif self.__join_type == "union_with_window":
            join_method = self.__join_dataframes_using_union_and_window

        else:
            raise Exception("Invalid join type")

        # optimization: same features/schema -> we don't have to load feature store and can only compute hash once and lit it
        registered_features = {col for col in feature_store.columns if col not in technical_columns}
        incoming_features = {*feature_list.get_names()}

        if registered_features == incoming_features:
            features_hash = hashlib.md5("`".join(feature_list.get_names()).encode()).hexdigest()

            return join_method(results, pk_columns).select(
                entity.id_column,
                entity.time_column,
                f.lit(features_hash).alias(get_rainbow_table_hash_column().name),
                f.lit(f.array(*map(f.lit, feature_list.get_names()))).alias(get_rainbow_table_features_column().name),
                *feature_list.get_names(),
            )

        feature_dfs = []
        duplicate_columns = []

        for i, df in enumerate(results):
            features = [col for col in df.columns if col not in technical_columns]
            feature_dfs.append(df.withColumn(f"new_columns_{i}", f.array(*map(f.lit, features))).alias(f"df{i}"))
            duplicate_columns.append(f.col(f"new_columns_{i}"))

        joined_results = (
            join_method(feature_dfs, pk_columns)
            .withColumn("temp", f.array(*duplicate_columns))
            .withColumn("new_columns", f.flatten(f.filter("temp", lambda x: x.isNotNull())))
            .select(
                entity.id_column,
                entity.time_column,
                *feature_list.get_names(),
                "new_columns",
            )
        )

        return (
            joined_results.join(feature_store.select(technical_columns), on=pk_columns, how="left")
            .join(rainbow_table, on=get_rainbow_table_hash_column().name, how="left")
            .withColumn("computed_columns", f.when(f.col("computed_columns").isNull(), f.array()).otherwise(f.col("computed_columns")))
            .withColumn("columns_union", f.array_sort(f.array_union("computed_columns", "new_columns")))
            .withColumn("new_features_hash", f.md5(f.concat_ws("`", "columns_union")))
            .drop("features_hash", "computed_columns")
            .withColumnRenamed("new_features_hash", "features_hash")
            .withColumnRenamed("columns_union", "computed_columns")
        )

    def __join_dataframes_using_left_join(self, dfs: List[DataFrame], join_columns: List[str]) -> DataFrame:
        join_batch_counter = 0
        id_dataframes = [df.select(join_columns) for df in dfs]
        unique_ids_df = reduce(lambda df1, df2: df1.unionByName(df2), id_dataframes).distinct().cache()
        joined_df = unique_ids_df

        for df in dfs:
            join_batch_counter += 1
            joined_df = joined_df.join(df, on=join_columns, how="left")

            if join_batch_counter == self.__join_batch_size:
                joined_df = joined_df.checkpoint()
                join_batch_counter = 0

        return joined_df

    def __join_dataframes_using_union_and_window(self, dfs: List[DataFrame], join_columns: List[str]) -> DataFrame:
        window = Window.partitionBy(*join_columns).rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
        union_df = reduce(lambda df1, df2: df1.unionByName(df2, allowMissingColumns=True), dfs)
        features = [col for col in union_df.columns if col not in join_columns]

        return (
            union_df.select(
                *join_columns,
                *[f.first(feature, ignorenulls=True).over(window).alias(feature) for feature in features],
            )
            .groupBy(join_columns)
            .agg(*[f.first(feature).alias(feature) for feature in features])
        )

    def __load_feature_store(self, entity: Entity) -> DataFrame:
        if not self.__features_reader.exists(entity.name):
            return self.__empty_dataframe_creator.create(get_feature_store_initial_schema(entity))

        return self.__features_reader.read(entity.name)

    def __load_rainbow_table(self, entity: Entity) -> DataFrame:
        if not self.__rainbow_table_manager.exists(entity.name):
            return self.__empty_dataframe_creator.create(get_rainbow_table_schema())

        return self.__rainbow_table_manager.get(entity.name)
