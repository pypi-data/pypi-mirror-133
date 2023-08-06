from typing import List, Optional, Union
from logging import Logger
from featurestorebundle.db.TableNames import TableNames
from featurestorebundle.entity.Entity import Entity
from featurestorebundle.delta.feature.DeltaFeaturesManager import DeltaFeaturesManager
from featurestorebundle.delta.PathExistenceChecker import PathExistenceChecker
from featurestorebundle.delta.EmptyDataFrameCreator import EmptyDataFrameCreator
from featurestorebundle.feature.reader.FeaturesReaderInterface import FeaturesReaderInterface
from featurestorebundle.delta.feature.schema import get_feature_store_initial_schema


class DeltaPathFeaturesReader(FeaturesReaderInterface):
    def __init__(
        self,
        logger: Logger,
        table_names: TableNames,
        feature_manager: DeltaFeaturesManager,
        path_existence_checker: PathExistenceChecker,
        empty_dataframe_creator: EmptyDataFrameCreator,
    ):
        self.__logger = logger
        self.__table_names = table_names
        self.__features_manager = feature_manager
        self.__path_existence_checker = path_existence_checker
        self.__empty_dataframe_creator = empty_dataframe_creator

    def read(self, entity: Union[Entity, str], features: Optional[List[str]] = None):
        features = features or []

        if isinstance(entity, Entity):
            entity = entity.name

        path = self.__table_names.get_features_path(entity)

        self.__logger.info(f"Reading features from path {path}")

        return self.__features_manager.get_features(f"delta.`{path}`", features)

    def read_safe(self, entity: Entity, features: Optional[List[str]] = None):
        features = features or []

        path = self.__table_names.get_features_path(entity.name)

        if not self.exists(entity):
            return self.__empty_dataframe_creator.create(get_feature_store_initial_schema(entity))

        return self.__features_manager.get_features(f"delta.`{path}`", features)

    def exists(self, entity: Union[Entity, str]):
        if isinstance(entity, Entity):
            entity = entity.name

        path = self.__table_names.get_features_path(entity)

        return self.__path_existence_checker.exists(path)
