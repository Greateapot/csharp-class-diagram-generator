from typing import Callable, TypeVar

T = TypeVar("T")


def clear_code(code: str) -> str:
    return " ".join(filter(lambda x: x, code.split(" ")))


def first_where(items: list[T], condition: Callable[[T], bool]) -> T | None:
    for item in items:
        if condition(item):
            return item


def type2mermaid(type: str) -> str:
    return type.replace("<", "~").replace(">", "~")


__all__ = (
    clear_code,
    first_where,
    type2mermaid,
)
