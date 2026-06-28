from typing import Optional

from errors import SparrowTypeError
from semantic.types_ import BoolType, FuncType, IntType, NothingType, Type


class TypeEnvironment:
    def __init__(self, parent: Optional["TypeEnvironment"] = None):
        self.parent = parent
        self.symbols: dict[str, Type] = {}

    def exists(self, name: str) -> bool:
        if name in self.symbols:
            return True
        if self.parent is not None:
            return self.parent.exists(name)
        return False

    def symbolStr(self, type: Type) -> str:
        symStr = ""
        match type:
            case IntType() | BoolType() | NothingType():
                symStr = "Variable"
            case FuncType():
                symStr = "Function"
            case _:
                symStr = "Symbol"
        return symStr

    def declare(self, name: str, type: Type, start: int, end: int) -> None:
        if name in self.symbols:
            raise SparrowTypeError(
                f"{self.symbolStr(type)} {name!r} is already declared in this scope",
                start,
                end,
            )

        self.symbols[name] = type

    def type(self, name: str, start: int, end: int) -> Type:
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent is not None:
            return self.parent.type(name, start, end)
        else:
            raise SparrowTypeError(
                f"Failed to access undeclared symbol {name!r}",
                start,
                end,
            )
