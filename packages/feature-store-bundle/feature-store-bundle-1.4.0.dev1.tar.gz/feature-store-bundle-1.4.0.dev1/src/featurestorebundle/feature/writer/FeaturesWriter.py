from featurestorebundle.feature.writer.FeaturesWriterInterface import FeaturesWriterInterface
from featurestorebundle.feature.FeaturesStorage import FeaturesStorage


class FeaturesWriter:
    def __init__(self, feature_writer: FeaturesWriterInterface):
        self.__feature_writer = feature_writer

    def write(self, features_storage: FeaturesStorage):
        self.__feature_writer.write(features_storage)
