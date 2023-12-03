class PrettyPrintMixin:
    def __str__(self) -> str:
        body = ", ".join(
            [
                f"{name}={repr(getattr(self, name))}"
                for name in self.__dict__
                if not name.startswith("_")
            ]
        )
        return f"{self.__class__.__name__}({body})"

    def __repr__(self) -> str:
        return str(self)
