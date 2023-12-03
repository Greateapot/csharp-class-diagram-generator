from __future__ import annotations

from enum import StrEnum

from .utils import clear_code


class Annotation(StrEnum):
    Interface = "<<Interface>>"
    Abstract = "<<Abstract>>"
    Enumeration = "<<Enumeration>>"

    def parse(code: str) -> Annotation | None:
        match clear_code(code):
            case "interface":
                return Annotation.Interface
            case "abstract class":
                return Annotation.Abstract
            case "enum":
                return Annotation.Enumeration
            case _:
                return None


class Visibility(StrEnum):
    Public = "+"
    Private = "-"
    Protected = "#"
    Internal = "~"

    def parse(code: str) -> Visibility | None:
        match clear_code(code):
            case "public":
                return Visibility.Public
            case "protected":
                return Visibility.Protected
            case "private" | "" | None:
                return Visibility.Private
            case "internal":
                return Visibility.Internal
            case _:
                return None


class MethodModifier(StrEnum):
    Static = "static"
    Abstract = "abstract"
    Virtual = "virtual"
    Override = "override"
    OverrideSealed = "override sealed"
    New = "new"

    def parse(code: str) -> MethodModifier | None:
        match clear_code(code):
            case "static":
                return MethodModifier.Static
            case "abstract":
                return MethodModifier.Abstract
            case "virtual":
                return MethodModifier.Virtual
            case "override":
                return MethodModifier.Override
            case "override sealed":
                return MethodModifier.OverrideSealed
            case "new":
                return MethodModifier.New
            case _:
                return None


class PropertyModifier(StrEnum):
    Static = "static"

    def parse(code: str) -> PropertyModifier | None:
        match clear_code(code):
            case "static":
                return PropertyModifier.Static
            case _:
                return None


class ParameterModifier(StrEnum):
    Out = "out"
    In = "in"
    Ref = "ref"
    RefReadOnly = "ref readonly"
    Params = "params"

    def parse(code: str) -> ParameterModifier | None:
        match clear_code(code):
            case "in":
                return ParameterModifier.In
            case "out":
                return ParameterModifier.Out
            case "ref":
                return ParameterModifier.Ref
            case "ref readonly":
                return ParameterModifier.RefReadOnly
            case "params":
                return ParameterModifier.Params
            case _:
                return None


class ClassRelationship(StrEnum):
    Inheritance = "<|--"
    Aggregation = "o--"
    Association = "-->"
    Dependency = "..>"
    Realization = "..|>"


__all__ = (
    Annotation,
    Visibility,
    MethodModifier,
    PropertyModifier,
    ParameterModifier,
    ClassRelationship,
)
