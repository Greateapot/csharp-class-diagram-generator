from __future__ import annotations

from .abc import AbcModel
from .pretty_print_mixin import PrettyPrintMixin

from cscdg.enums import ClassRelationship


class Relation(AbcModel, PrettyPrintMixin):
    def __init__(
        self,
        from_name: str,
        to_name: str,
        type: ClassRelationship,
    ) -> None:
        self.from_name = from_name
        self.to_name = to_name
        self.type = type

    def to_mermaid(self) -> str:
        return f"{self.from_name} {self.type} {self.to_name}"
