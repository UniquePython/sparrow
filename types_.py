from dataclasses import dataclass
from typing import Union

Type = Union["IntType", "BoolType", "NothingType", "FuncType"]


@dataclass(frozen=True)
class IntType:
    def __repr__(self) -> str:
        return "Int"


@dataclass(frozen=True)
class BoolType:
    def __repr__(self) -> str:
        return "Bool"


@dataclass(frozen=True)
class NothingType:
    def __repr__(self) -> str:
        return "Nothing"


@dataclass(frozen=True)
class FuncType:
    paramTypes: tuple[Type, ...]
    returnType: Type

    def __repr__(self) -> str:
        params = ", ".join(str(p) for p in self.paramTypes)
        return f"({params}) -> {self.returnType}"


Int = IntType()
Bool = BoolType()
Nothing = NothingType()
