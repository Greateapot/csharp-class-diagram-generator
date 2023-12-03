from __future__ import annotations

from .abc import AbcModel
from .pretty_print_mixin import PrettyPrintMixin
from .clazz import Class

from cscdg.patterns import findall, namespace_pattern
from cscdg.utils import first_where


class Namespace(AbcModel, PrettyPrintMixin):
    def __init__(
        self,
        name: str,
        classes: list[Class],
    ) -> None:
        self.name = name
        self.classes = classes

    def minimize(self) -> None:
        classes: list[Class] = list()

        for clazz in self.classes:
            item = first_where(classes, lambda x: x.name == clazz.name)
            if item is not None:
                item.properties += clazz.properties
                item.methods += clazz.methods
            else:
                classes.append(clazz)

        self.classes = classes

    def to_mermaid(self) -> str:
        mermaids: list[str] = [i.to_mermaid() for i in self.classes]
        body = "\n\t".join(mermaids)
        return f"namespace {self.name} {{\n\t{body}\n}}"

    @staticmethod
    def parse(code: str) -> list[Namespace]:
        namespaces: list[Namespace] = list()

        for match in findall(namespace_pattern, code):
            namespace = Namespace(
                name=match[0],
                classes=Class.parse(match[1]),
            )
            namespaces.append(namespace)

        return namespaces
