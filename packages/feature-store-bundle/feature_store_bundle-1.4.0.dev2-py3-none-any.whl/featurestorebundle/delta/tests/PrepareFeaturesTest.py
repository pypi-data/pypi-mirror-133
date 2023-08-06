import unittest
import hashlib
import datetime as dt
from pyspark.sql import types as t
from pyspark.sql import DataFrame
from pyspark.sql.window import Window
from pyfonycore.bootstrap import bootstrapped_container
from featurestorebundle.entity.Entity import Entity
from featurestorebundle.feature.Feature import Feature
from featurestorebundle.feature.FeatureList import FeatureList
from featurestorebundle.feature.FeatureTemplate import FeatureTemplate
from featurestorebundle.feature.FeaturesPreparer import FeaturesPreparer
from featurestorebundle.feature.FeaturesStorage import FeaturesStorage
from featurestorebundle.delta.feature.schema import get_feature_store_initial_schema, get_rainbow_table_schema
from featurestorebundle.test.PySparkTestCase import PySparkTestCase


class PrepareFeaturesTestCase(PySparkTestCase):
    def setUp(self) -> None:
        self.__entity = Entity(
            name="client_test",
            id_column="client_id",
            id_column_type=t.StringType(),
            time_column="run_date",
            time_column_type=t.DateType(),
        )

        self.__container = bootstrapped_container.init("test")
        self.__features_preparer: FeaturesPreparer = self.__container.get(FeaturesPreparer)
        self.__feature_store_merge_columns = [self.__entity.id_column, self.__entity.time_column, "features_hash"]
        self.__rainbow_table_merge_columns = ["features_hash", "computed_columns"]

    def test_simple(self):
        features_storage = FeaturesStorage(self.__entity)
        feature_store = self.spark.createDataFrame([], get_feature_store_initial_schema(self.__entity))
        rainbow_table = self.spark.createDataFrame([], get_rainbow_table_schema())

        df_1 = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 1), "c1f1", "c1f2"],
                ["2", dt.date(2020, 1, 1), "c2f1", "c2f2"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "f1", "f2"],
        )

        feature_list_1 = FeatureList(
            [
                Feature(self.__entity.name, "f1", "this is feature 1", "string", {}, FeatureTemplate("f1", "this is feature 1")),
                Feature(self.__entity.name, "f2", "this is feature 2", "string", {}, FeatureTemplate("f2", "this is feature 2")),
            ]
        )

        features_storage.add(df_1, feature_list_1)

        features_data, rainbow_data = self.__features_preparer.prepare(features_storage, feature_store, rainbow_table)

        expected_features_data = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 1), hashlib.md5("f1`f2".encode()).hexdigest(), "c1f1", "c1f2"],
                ["2", dt.date(2020, 1, 1), hashlib.md5("f1`f2".encode()).hexdigest(), "c2f1", "c2f2"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "f1", "f2"],
        )

        expected_rainbow_data = self.spark.createDataFrame(
            [
                [hashlib.md5("f1`f2".encode()).hexdigest(), ["f1", "f2"]],
            ],
            ["features_hash", "computed_columns"],
        )

        features_data = features_data.orderBy(self.__entity.time_column, self.__entity.id_column)
        expected_features_data = expected_features_data.orderBy(self.__entity.time_column, self.__entity.id_column)
        rainbow_data = rainbow_data.orderBy("features_hash")
        expected_rainbow_data = expected_rainbow_data.orderBy("features_hash")

        self.assertEqual(features_data.collect(), expected_features_data.collect())
        self.assertEqual(rainbow_data.collect(), expected_rainbow_data.collect())

    def test_two_feature_results(self):
        features_storage = FeaturesStorage(self.__entity)
        feature_store = self.spark.createDataFrame([], get_feature_store_initial_schema(self.__entity))
        rainbow_table = self.spark.createDataFrame([], get_rainbow_table_schema())

        df_1 = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 1), "c1f1", "c1f2"],
                ["2", dt.date(2020, 1, 1), "c2f1", "c2f2"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "f1", "f2"],
        )

        feature_list_1 = FeatureList(
            [
                Feature(self.__entity.name, "f1", "this is feature 1", "string", {}, FeatureTemplate("f1", "this is feature 1")),
                Feature(self.__entity.name, "f2", "this is feature 2", "string", {}, FeatureTemplate("f2", "this is feature 2")),
            ]
        )

        df_2 = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 1), "c1f3"],
                ["2", dt.date(2020, 1, 1), "c2f3"],
                ["3", dt.date(2020, 1, 1), "c3f3"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "f3"],
        )

        feature_list_2 = FeatureList(
            [
                Feature(self.__entity.name, "f3", "this is feature 3", "string", {}, FeatureTemplate("f3", "this is feature 3")),
            ]
        )

        features_storage.add(df_1, feature_list_1)
        features_storage.add(df_2, feature_list_2)

        features_data, rainbow_data = self.__features_preparer.prepare(features_storage, feature_store, rainbow_table)

        expected_features_data = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 1), hashlib.md5("f1`f2`f3".encode()).hexdigest(), "c1f1", "c1f2", "c1f3"],
                ["2", dt.date(2020, 1, 1), hashlib.md5("f1`f2`f3".encode()).hexdigest(), "c2f1", "c2f2", "c2f3"],
                ["3", dt.date(2020, 1, 1), hashlib.md5("f1`f2`f3".encode()).hexdigest(), None, None, "c3f3"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "f1", "f2", "f3"],
        )

        expected_rainbow_data = self.spark.createDataFrame(
            [
                [hashlib.md5("f1`f2`f3".encode()).hexdigest(), ["f1", "f2", "f3"]],
            ],
            ["features_hash", "computed_columns"],
        )

        features_data = features_data.orderBy(self.__entity.time_column, self.__entity.id_column)
        expected_features_data = expected_features_data.orderBy(self.__entity.time_column, self.__entity.id_column)
        rainbow_data = rainbow_data.orderBy("features_hash")
        expected_rainbow_data = expected_rainbow_data.orderBy("features_hash")

        self.assertEqual(features_data.collect(), expected_features_data.collect())
        self.assertEqual(rainbow_data.collect(), expected_rainbow_data.collect())

    def test_add_new_feature(self):
        features_storage = FeaturesStorage(self.__entity)

        feature_store = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 1), hashlib.md5("f1`f2".encode()).hexdigest(), "c1f1", "c1f2"],
                ["2", dt.date(2020, 1, 1), hashlib.md5("f1`f2".encode()).hexdigest(), "c2f1", "c2f2"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "features_hash", "f1", "f2"],
        )

        rainbow_table = self.spark.createDataFrame(
            [
                [hashlib.md5("f1`f2".encode()).hexdigest(), ["f1", "f2"]],
            ],
            ["features_hash", "computed_columns"],
        )

        df_1 = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 2), "c1f3"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "f3"],
        )

        feature_list_1 = FeatureList(
            [
                Feature(self.__entity.name, "f3", "this is feature 3", "string", {}, FeatureTemplate("f3", "this is feature 3")),
            ]
        )

        features_storage.add(df_1, feature_list_1)

        features_data, rainbow_data = self.__features_preparer.prepare(features_storage, feature_store, rainbow_table)

        feature_store_after_merge = feature_store.join(features_data, on=self.__feature_store_merge_columns, how="outer")
        rainbow_table_after_merge = rainbow_table.join(rainbow_data, on=self.__rainbow_table_merge_columns, how="outer")

        expected_feature_store = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 1), hashlib.md5("f1`f2".encode()).hexdigest(), "c1f1", "c1f2", None],
                ["2", dt.date(2020, 1, 1), hashlib.md5("f1`f2".encode()).hexdigest(), "c2f1", "c2f2", None],
                ["1", dt.date(2020, 1, 2), hashlib.md5("f3".encode()).hexdigest(), None, None, "c1f3"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "f1", "f2", "f3"],
        )

        expected_rainbow_table = self.spark.createDataFrame(
            [
                [hashlib.md5("f1`f2".encode()).hexdigest(), ["f1", "f2"]],
                [hashlib.md5("f3".encode()).hexdigest(), ["f3"]],
            ],
            ["features_hash", "computed_columns"],
        )

        feature_store_after_merge = feature_store_after_merge.orderBy(self.__entity.time_column, self.__entity.id_column)
        expected_feature_store = expected_feature_store.orderBy(self.__entity.time_column, self.__entity.id_column)
        rainbow_table_after_merge = rainbow_table_after_merge.orderBy("features_hash")
        expected_rainbow_table = expected_rainbow_table.orderBy("features_hash")

        self.assertEqual(feature_store_after_merge.collect(), expected_feature_store.collect())
        self.assertEqual(rainbow_table_after_merge.collect(), expected_rainbow_table.collect())

    def test_backfill_feature(self):
        features_storage = FeaturesStorage(self.__entity)

        feature_store = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 1), hashlib.md5("f1`f2".encode()).hexdigest(), "c1f1", "c1f2", None],
                ["2", dt.date(2020, 1, 1), hashlib.md5("f1`f2".encode()).hexdigest(), "c2f1", "c2f2", None],
                ["1", dt.date(2020, 1, 2), hashlib.md5("f3".encode()).hexdigest(), None, None, "c1f3"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "features_hash", "f1", "f2", "f3"],
        )

        rainbow_table = self.spark.createDataFrame(
            [
                [hashlib.md5("f1`f2".encode()).hexdigest(), ["f1", "f2"]],
                [hashlib.md5("f3".encode()).hexdigest(), ["f3"]],
            ],
            ["features_hash", "computed_columns"],
        )

        df_1 = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 1), "c1f3"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "f3"],
        )

        feature_list_1 = FeatureList(
            [
                Feature(self.__entity.name, "f3", "this is feature 3", "string", {}, FeatureTemplate("f3", "this is feature 3")),
            ]
        )

        features_storage.add(df_1, feature_list_1)

        features_data, rainbow_data = self.__features_preparer.prepare(features_storage, feature_store, rainbow_table)

        feature_store_after_merge = self.__delta_merge(feature_store, features_data, [self.__entity.id_column, self.__entity.time_column])
        rainbow_table_after_merge = rainbow_table.join(rainbow_data, on=self.__rainbow_table_merge_columns, how="outer")
        feature_store_after_merge.show()
        expected_feature_store = self.spark.createDataFrame(
            [
                ["1", dt.date(2020, 1, 1), hashlib.md5("f1`f2`f3".encode()).hexdigest(), "c1f1", "c1f2", "c1f3"],
                ["2", dt.date(2020, 1, 1), hashlib.md5("f1`f2".encode()).hexdigest(), "c2f1", "c2f2", None],
                ["1", dt.date(2020, 1, 2), hashlib.md5("f3".encode()).hexdigest(), None, None, "c1f3"],
            ],
            [self.__entity.id_column, self.__entity.time_column, "f1", "f2", "f3"],
        )

        expected_rainbow_table = self.spark.createDataFrame(
            [
                [hashlib.md5("f1`f2`f3".encode()).hexdigest(), ["f1", "f2", "f3"]],
                [hashlib.md5("f1`f2".encode()).hexdigest(), ["f1", "f2"]],
                [hashlib.md5("f3".encode()).hexdigest(), ["f3"]],
            ],
            ["features_hash", "computed_columns"],
        )

        feature_store_after_merge = feature_store_after_merge.orderBy(self.__entity.time_column, self.__entity.id_column)
        expected_feature_store = expected_feature_store.orderBy(self.__entity.time_column, self.__entity.id_column)
        rainbow_table_after_merge = rainbow_table_after_merge.orderBy("features_hash")
        expected_rainbow_table = expected_rainbow_table.orderBy("features_hash")

        self.assertEqual(feature_store_after_merge.collect(), expected_feature_store.collect())
        self.assertEqual(rainbow_table_after_merge.collect(), expected_rainbow_table.collect())

    def __delta_merge(self, target: DataFrame, source: DataFrame, join_columns: list):  # noqa
        target_columns = target.columns
        source_columns = source.columns
        duplicate_columns = list((set(target_columns) & set(source_columns)) - set(join_columns))
        unique_columns = list((set(target_columns) | set(source_columns)) - set(join_columns) - set(duplicate_columns))
        window = Window.partitionBy(join_columns).rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)

        return (
            target.alias("target").join(source.alias("source"), on=join_columns, how="outer")
            .select(
                *join_columns,

            )
        )


if __name__ == "__main__":
    unittest.main()
