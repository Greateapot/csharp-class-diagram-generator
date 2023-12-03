from __future__ import annotations

from .abc import AbcModel
from .pretty_print_mixin import PrettyPrintMixin

from cscdg.enums import PropertyModifier, Visibility
from cscdg.patterns import findall, property_pattern
from cscdg.utils import type2mermaid


class Property(AbcModel, PrettyPrintMixin):
    def __init__(
        self,
        name: str,
        type: str,
        modifier: PropertyModifier = None,
        visibility: Visibility = Visibility.Private,
    ) -> None:
        self.name = name
        self.type = type
        self.modifier = modifier
        self.visibility = visibility

    def to_mermaid(self) -> str:
        result = f"{type2mermaid(self.type)} {self.name}"
        if self.modifier is PropertyModifier.Static:
            result += "$"
        return result

    @staticmethod
    def parse(code: str) -> list[Property]:
        properties: list[Property] = list()

        for match in findall(property_pattern, code):
            property = Property(
                visibility=Visibility.parse(match[0]),
                modifier=PropertyModifier.parse(match[1]),
                type=match[2],
                name=match[4],
            )
            properties.append(property)

        return properties
