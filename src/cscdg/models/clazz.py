from __future__ import annotations

from .abc import AbcModel
from .pretty_print_mixin import PrettyPrintMixin
from .property import Property
from .method import Method

from cscdg.enums import Annotation
from cscdg.patterns import findall, class_pattern


class Class(AbcModel, PrettyPrintMixin):
    def __init__(
        self,
        name: str,
        properties: list[Property],
        methods: list[Method],
        annotation: Annotation = None,
        relations: str = None,
    ) -> None:
        self.name = name
        self.annotation = annotation
        self.relations = relations
        self.properties = properties
        self.methods = methods

    def to_mermaid(self) -> str:
        mermaids: list[str] = []

        if self.annotation is not None:
            mermaids.append(str(self.annotation))
        mermaids += [i.to_mermaid() for i in self.properties]
        mermaids += [i.to_mermaid() for i in self.methods]

        body = "\n\t".join(mermaids)
        return f"class {self.name} {{\n\t{body}\n\t}}"

    @staticmethod
    def parse(code: str) -> list[Class]:
        classes: list[Class] = list()

        for match in findall(class_pattern, code):
            clazz = Class(
                annotation=Annotation.parse(match[0]),
                name=match[1],
                relations=match[3],
                properties=Property.parse(match[4]),
                methods=Method.parse(match[4], match[1]),
            )
            classes.append(clazz)

        return classes
