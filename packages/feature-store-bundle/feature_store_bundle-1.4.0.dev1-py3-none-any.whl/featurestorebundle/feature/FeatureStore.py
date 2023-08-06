from typing import List, Optional
from featurestorebundle.feature.reader.FeaturesReaderInterface import FeaturesReaderInterface
from featurestorebundle.metadata.reader.MetadataReaderInterface import MetadataReaderInterface


class FeatureStore:
    def __init__(
        self,
        features_reader: FeaturesReaderInterface,
        metadata_reader: MetadataReaderInterface,
    ):
        self.__features_reader = features_reader
        self.__metadata_reader = metadata_reader

    def get(self, entity_name: str, feature_names: Optional[List[str]] = None):
        return self.__features_reader.read(entity_name, feature_names)

    def get_latest(self, entity_name: str, feature_names: Optional[List[str]] = None):
        return self.__features_reader.read(entity_name, feature_names)

    def get_historized(self, entity_name: str, feature_names: Optional[List[str]] = None):
        return self.__features_reader.read(entity_name, feature_names)

    def get_metadata(self, entity_name: Optional[str] = None):
        return self.__metadata_reader.read(entity_name)
