from dataclasses import dataclass
from typing import Tuple


@dataclass
class VersionedType:
    name: str
    version: int

    def __key(self) -> Tuple[str, int]:
        return (self.name, self.version)

    def __hash__(self) -> int:
        return hash(self.__key)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, VersionedType):
            return self.__key == other.__key
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, VersionedType):
            if self.name == other.name:
                return self.version < other.version
            return self.name < other.name
        raise NotImplementedError
