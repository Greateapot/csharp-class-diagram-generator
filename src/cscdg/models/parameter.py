from __future__ import annotations

from .abc import AbcModel
from .pretty_print_mixin import PrettyPrintMixin

from cscdg.enums import ParameterModifier
from cscdg.patterns import findall, parameters_pattern
from cscdg.utils import type2mermaid


class Parameter(AbcModel, PrettyPrintMixin):
    def __init__(
        self,
        name: str,
        type: str,
        modifier: ParameterModifier,
    ) -> None:
        self.name = name
        self.type = type
        self.modifier = modifier

    def to_mermaid(self) -> str:
        return f"{type2mermaid(self.type)} {self.name}"

    @staticmethod
    def parse(code: str) -> list[Parameter]:
        parameters: list[Parameter] = list()

        for match in findall(parameters_pattern, code):
            parameter = Parameter(
                modifier=ParameterModifier.parse(match[0]),
                type=match[1],
                name=match[3],
            )
            parameters.append(parameter)

        return parameters
