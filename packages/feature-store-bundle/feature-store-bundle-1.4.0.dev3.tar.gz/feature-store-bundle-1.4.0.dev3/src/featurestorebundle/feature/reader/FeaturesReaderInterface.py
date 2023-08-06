from abc import ABC, abstractmethod
from typing import List, Optional, Union
from featurestorebundle.entity.Entity import Entity


class FeaturesReaderInterface(ABC):
    @abstractmethod
    def read(self, entity: Union[Entity, str], features: Optional[List[str]] = None):
        pass

    @abstractmethod
    def read_safe(self, entity: Entity, features: Optional[List[str]] = None):
        pass

    @abstractmethod
    def exists(self, entity: Union[Entity, str]):
        pass
