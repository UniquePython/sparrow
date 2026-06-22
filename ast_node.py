from dataclasses import dataclass
from enum import Enum, auto
from typing import Union


class BinaryOp(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()


Expr = Union["NumberLiteral", "BinaryExpr"]


@dataclass(frozen=True)
class NumberLiteral:
    value: int
    start: int
    end: int


@dataclass(frozen=True)
class BinaryExpr:
    operator: BinaryOp
    left: Expr
    right: Expr
    start: int
    end: int
