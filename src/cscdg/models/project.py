from __future__ import annotations

import os

from .abc import AbcModel
from .pretty_print_mixin import PrettyPrintMixin
from .namespace import Namespace
from .clazz import Class
from .relation import Relation

from cscdg.enums import Annotation, ClassRelationship
from cscdg.utils import first_where


class Project(AbcModel, PrettyPrintMixin):
    def __init__(
        self,
        path: str,
        namespaces: list[Namespace],
    ) -> None:
        self.path = path
        self.namespaces = namespaces

    def minimize(self) -> None:
        namespaces: list[Namespace] = list()

        for namespace in self.namespaces:
            item = first_where(namespaces, lambda x: x.name == namespace.name)
            if item is not None:
                item.classes += namespace.classes
            else:
                namespaces.append(namespace)

        self.namespaces = namespaces

        for namespace in self.namespaces:
            namespace.minimize()

    def to_mermaid(self) -> str:
        mermaids: list[str] = [i.to_mermaid() for i in self.namespaces]
        classes: list[Class] = [
            clazz for namespace in self.namespaces for clazz in namespace.classes
        ]
        clazz_names = [clazz.name for clazz in classes]
        relations: list[Relation] = []

        for clazz in classes:
            crs: list[str] = list(
                filter(
                    lambda x: x, map(lambda x: x.strip(), clazz.relations.split(","))
                )
            )
            for cr in crs:
                if cr.startswith("I") and len(cr) > 1 and cr[1].isupper():
                    relations.append(
                        Relation(
                            from_name=clazz.name.replace("<", "~").replace(">", "~"),
                            to_name=cr.replace("<", "~").replace(">", "~"),
                            type=ClassRelationship.Realization,
                        )
                    )
                    if cr not in clazz_names:
                        clazz_names.append(cr)
                        mermaids.append(
                            Class(cr.replace("<", "~").replace(">", "~"), [], [], Annotation.Interface).to_mermaid()
                        )
                else:
                    relations.append(
                        Relation(
                            from_name=cr.replace("<", "~").replace(">", "~"),
                            to_name=clazz.name.replace("<", "~").replace(">", "~"),
                            type=ClassRelationship.Inheritance,
                        )
                    )

            for other in classes:
                for method in other.methods:
                    for parameter in method.parameters:
                        if clazz.name in parameter.type:
                            relations.append(
                                Relation(
                                    from_name=other.name,
                                    to_name=clazz.name,
                                    type=ClassRelationship.Dependency,
                                )
                            )

        header = "\n".join(
            [clazz.name for clazz in classes]
            + list(set([i.to_mermaid() for i in relations]))
        )
        body = "\n\t".join(mermaids)
        return f"```mermaid\nclassDiagram\n{header}\n{body}\n```"

    @staticmethod
    def parse(path: str) -> Project:
        project = Project(
            path=path,
            namespaces=[],
        )

        for dirpath, _, filenames in os.walk(path):
            if dirpath.startswith(
                os.path.join(path, "bin"),
            ) or dirpath.startswith(
                os.path.join(path, "obj"),
            ):
                continue

            for filename in filenames:
                with open(
                    os.path.join(dirpath, filename), "r", encoding="utf-8"
                ) as file:
                    project.namespaces += Namespace.parse(file.read())

        project.minimize()

        return project
