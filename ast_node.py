from dataclasses import dataclass
from enum import Enum, auto
from typing import Union


class BinaryOp(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    EQEQ = auto()
    NEQ = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()


class UnaryOp(Enum):
    NEG = auto()


Expr = Union[
    "NumberLiteral", "BooleanLiteral", "BinaryExpr", "UnaryExpr", "IdentifierExpr"
]


@dataclass(frozen=True)
class NumberLiteral:
    value: int
    start: int
    end: int


@dataclass(frozen=True)
class BooleanLiteral:
    value: bool
    start: int
    end: int


@dataclass(frozen=True)
class BinaryExpr:
    operator: BinaryOp
    left: Expr
    right: Expr
    start: int
    end: int


@dataclass(frozen=True)
class UnaryExpr:
    operator: UnaryOp
    operand: Expr
    start: int
    end: int


@dataclass(frozen=True)
class IdentifierExpr:
    name: str
    start: int
    end: int


Stmt = Union["AssignStmt", "ExprStmt"]


@dataclass(frozen=True)
class AssignStmt:
    name: str
    value: Expr
    start: int
    end: int


@dataclass(frozen=True)
class ExprStmt:
    expr: Expr
    start: int
    end: int
