from __future__ import annotations

from .abc import AbcModel
from .pretty_print_mixin import PrettyPrintMixin
from .parameter import Parameter

from cscdg.enums import Visibility, MethodModifier
from cscdg.patterns import findall, method_pattern
from cscdg.utils import type2mermaid


class Method(AbcModel, PrettyPrintMixin):
    def __init__(
        self,
        name: str,
        parameters: list[Parameter],
        return_type: str = "",
        modifier: MethodModifier = None,
        visibility: Visibility = Visibility.Private,
    ) -> None:
        self.name = name
        self.return_type = return_type
        self.modifier = modifier
        self.parameters = parameters
        self.visibility = visibility

    def to_mermaid(self) -> str:
        result = (
            f"{self.visibility}{self.name}"
            f"({', '.join(map(lambda x: x.to_mermaid(), self.parameters))}) "
            f"{type2mermaid(self.return_type)}"
        )
        if self.modifier is MethodModifier.Abstract:
            result += "*"
        elif self.modifier is MethodModifier.Static:
            result += "$"
        return result

    @staticmethod
    def parse(code: str, class_name: str) -> list[Method]:
        methods: list[Method] = list()

        for match in findall(method_pattern, code):
            if match[1] != "":
                continue
            elif match[5] + match[6] == class_name:
                method = Method(
                    visibility=Visibility.parse(match[3]),
                    # return_type=match[3],
                    name=match[5] + match[6],
                    # modifier=MethodModifier.parse(match[2]),
                    parameters=Parameter.parse(match[7]),
                )
            else:
                method = Method(
                    visibility=Visibility.parse(match[0]),
                    return_type=match[3],
                    name=match[5] + match[6],
                    modifier=MethodModifier.parse(match[2]),
                    parameters=Parameter.parse(match[7]),
                )
            methods.append(method)

        return methods
