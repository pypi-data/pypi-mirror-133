from typing import List
from pyspark.sql import SparkSession
from featurestorebundle.feature.Feature import Feature
from featurestorebundle.feature.FeatureList import FeatureList


class DeltaFeaturesManager:
    def __init__(self, spark: SparkSession):
        self.__spark = spark

    def register(self, table_identifier: str, feature_list: FeatureList):
        def build_add_column_string(feature: Feature):
            return f'{feature.name} {feature.dtype} COMMENT "{feature.description}"'

        def build_add_columns_string(table_identifier, feature_list: FeatureList):
            add_column_sqls = [build_add_column_string(feature) for feature in feature_list.get_all()]
            return f"ALTER TABLE {table_identifier} ADD COLUMNS ({','.join(add_column_sqls)})"

        registered_feature_names = self.get_feature_names(table_identifier)
        unregistered_features = feature_list.get_unregistered(registered_feature_names)

        if not unregistered_features.empty():
            self.__spark.sql(build_add_columns_string(table_identifier, feature_list))

    def get_features(self, table_identifier: str, feature_names: List[str]):
        registered_feature_names_list = self.get_feature_names(table_identifier)

        if not feature_names:
            feature_names = registered_feature_names_list

        unregistered_features = set(feature_names) - set(registered_feature_names_list)

        if unregistered_features != set():
            raise Exception(f"Features {','.join(unregistered_features)} not registered")

        return self.get_values(table_identifier, feature_names)

    def get_feature_names(self, table_identifier: str) -> List[str]:
        column_definitions = self.__spark.sql(f"DESCRIBE TABLE {table_identifier}").collect()

        def find_separation_row(column_definitions):
            for i, row in enumerate(column_definitions):
                if row.col_name in ["", "# Partition Information"]:
                    return i

            return None

        feature_rows = column_definitions[3 : find_separation_row(column_definitions)]  # noqa: E203
        return [row.col_name for row in feature_rows]

    def get_values(self, table_identifier: str, feature_names: List[str]):
        df = self.__spark.read.table(table_identifier)

        return df.select(df.columns[:3] + feature_names)
