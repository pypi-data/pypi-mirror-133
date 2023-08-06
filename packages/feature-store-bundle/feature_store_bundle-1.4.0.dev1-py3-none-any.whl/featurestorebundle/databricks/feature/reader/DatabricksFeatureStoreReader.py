from typing import List, Optional
from logging import Logger
from featurestorebundle.db.TableNames import TableNames
from featurestorebundle.delta.feature.DeltaFeaturesManager import DeltaFeaturesManager
from featurestorebundle.delta.TableExistenceChecker import TableExistenceChecker
from featurestorebundle.feature.reader.FeaturesReaderInterface import FeaturesReaderInterface


class DatabricksFeatureStoreReader(FeaturesReaderInterface):
    def __init__(
        self,
        logger: Logger,
        table_names: TableNames,
        feature_manager: DeltaFeaturesManager,
        table_existence_checker: TableExistenceChecker,
    ):
        self.__logger = logger
        self.__table_names = table_names
        self.__features_manager = feature_manager
        self.__table_existence_checker = table_existence_checker

    def read(self, entity_name: str, feature_names: Optional[List[str]] = None):
        feature_names = feature_names or []

        full_table_name = self.__table_names.get_features_full_table_name(entity_name)

        self.__logger.info(f"Reading features from Databricks Feature Store table {full_table_name}")

        return self.__features_manager.get_features(full_table_name, feature_names)

    def exists(self, entity_name: str):
        full_table_name = self.__table_names.get_features_full_table_name(entity_name)

        return self.__table_existence_checker.exists(full_table_name)
