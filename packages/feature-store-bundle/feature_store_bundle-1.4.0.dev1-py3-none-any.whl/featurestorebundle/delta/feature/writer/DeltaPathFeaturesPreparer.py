from featurestorebundle.entity.Entity import Entity
from featurestorebundle.delta.PathCreator import PathCreator
from featurestorebundle.feature.FeatureList import FeatureList
from featurestorebundle.delta.feature.DeltaFeaturesManager import DeltaFeaturesManager
from featurestorebundle.delta.feature.schema import get_feature_store_initial_schema


class DeltaPathFeaturesPreparer:
    def __init__(
        self,
        path_creator: PathCreator,
        features_manager: DeltaFeaturesManager,
    ):
        self.__path_creator = path_creator
        self.__features_manager = features_manager

    def prepare(self, path: str, entity: Entity, current_feature_list: FeatureList):
        self.__path_creator.create_if_not_exists(path, get_feature_store_initial_schema(entity), entity.time_column)
        self.__features_manager.register(f"delta.`{path}`", current_feature_list)
