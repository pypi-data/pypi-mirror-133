from abc import ABC, abstractmethod
from typing import List, Optional


class FeaturesReaderInterface(ABC):
    @abstractmethod
    def read(self, entity_name: str, feature_names: Optional[List[str]] = None):
        pass

    @abstractmethod
    def exists(self, entity_name: str):
        pass
