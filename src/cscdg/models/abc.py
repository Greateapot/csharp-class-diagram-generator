from abc import ABC, abstractmethod


class AbcModel(ABC):
    @abstractmethod
    def to_mermaid(self) -> str:
        ...
