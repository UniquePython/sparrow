from dataclasses import dataclass
from typing import Union

Type = Union["IntType", "BoolType", "NothingType", "FuncType"]


@dataclass(frozen=True)
class IntType:
    pass


@dataclass(frozen=True)
class BoolType:
    pass


@dataclass(frozen=True)
class NothingType:
    pass


@dataclass(frozen=True)
class FuncType:
    paramTypes: tuple[Type, ...]
    returnType: Type
