from typing import List, Optional
from logging import Logger
from featurestorebundle.db.TableNames import TableNames
from featurestorebundle.delta.feature.DeltaFeaturesManager import DeltaFeaturesManager
from featurestorebundle.delta.PathExistenceChecker import PathExistenceChecker
from featurestorebundle.feature.reader.FeaturesReaderInterface import FeaturesReaderInterface


class DeltaPathFeaturesReader(FeaturesReaderInterface):
    def __init__(
        self,
        logger: Logger,
        table_names: TableNames,
        feature_manager: DeltaFeaturesManager,
        path_existence_checker: PathExistenceChecker,
    ):
        self.__logger = logger
        self.__table_names = table_names
        self.__features_manager = feature_manager
        self.__path_existence_checker = path_existence_checker

    def read(self, entity_name: str, feature_names: Optional[List[str]] = None):
        feature_names = feature_names or []

        path = self.__table_names.get_features_path(entity_name)

        self.__logger.info(f"Reading features from path {path}")

        return self.__features_manager.get_features(f"delta.`{path}`", feature_names)

    def exists(self, entity_name: str):
        path = self.__table_names.get_features_path(entity_name)

        return self.__path_existence_checker.exists(path)
