from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union


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
    NOT = auto()


Expr = Union[
    "NumberLiteral",
    "BoolLiteral",
    "BinaryExpr",
    "UnaryExpr",
    "IdentifierExpr",
    "FuncCallExpr",
]


@dataclass(frozen=True)
class NumberLiteral:
    value: int
    start: int
    end: int


@dataclass(frozen=True)
class BoolLiteral:
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


@dataclass(frozen=True)
class FuncCallExpr:
    name: str
    args: tuple[Expr, ...]
    start: int
    end: int


Stmt = Union[
    "AssignStmt",
    "ExprStmt",
    "IfStmt",
    "WhileStmt",
    "RepeatStmt",
    "StopStmt",
    "SkipStmt",
    "VarDeclStmt",
    "FuncDeclStmt",
]


@dataclass(frozen=True)
class AssignStmt:
    name: str
    value: Expr
    start: int
    end: int


@dataclass(frozen=True)
class VarDeclStmt:
    type: str
    name: str
    value: Expr
    start: int
    end: int


@dataclass(frozen=True)
class Param:
    type: str
    name: str
    start: int
    end: int


@dataclass(frozen=True)
class FuncDeclStmt:
    name: str
    params: tuple[Param, ...]
    returnType: str
    body: tuple[Stmt, ...]
    start: int
    end: int


@dataclass(frozen=True)
class ExprStmt:
    expr: Expr
    start: int
    end: int


@dataclass(frozen=True)
class ElifClause:
    condition: Expr
    body: tuple[Stmt, ...]
    start: int
    end: int


@dataclass(frozen=True)
class IfStmt:
    condition: Expr
    ifBody: tuple[Stmt, ...]
    elifClauses: Optional[tuple[ElifClause, ...]]
    elseBody: Optional[tuple[Stmt, ...]]
    start: int
    end: int


@dataclass(frozen=True)
class WhileStmt:
    condition: Expr
    body: tuple[Stmt, ...]
    onstop: Optional[tuple[Stmt, ...]]
    nostop: Optional[tuple[Stmt, ...]]
    start: int
    end: int


@dataclass(frozen=True)
class RepeatStmt:
    ntimes: Expr
    body: tuple[Stmt, ...]
    onstop: Optional[tuple[Stmt, ...]]
    nostop: Optional[tuple[Stmt, ...]]
    start: int
    end: int


@dataclass(frozen=True)
class StopStmt:
    start: int
    end: int


@dataclass(frozen=True)
class SkipStmt:
    start: int
    end: int
