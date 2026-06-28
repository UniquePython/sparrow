from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


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


class Expr:
    pass


@dataclass(frozen=True)
class NumberLiteral(Expr):
    value: int
    start: int
    end: int


@dataclass(frozen=True)
class BoolLiteral(Expr):
    value: bool
    start: int
    end: int


@dataclass(frozen=True)
class BinaryExpr(Expr):
    operator: BinaryOp
    left: Expr
    right: Expr
    start: int
    end: int


@dataclass(frozen=True)
class UnaryExpr(Expr):
    operator: UnaryOp
    operand: Expr
    start: int
    end: int


@dataclass(frozen=True)
class IdentifierExpr(Expr):
    name: str
    start: int
    end: int


@dataclass(frozen=True)
class FuncCallExpr(Expr):
    name: str
    args: tuple[Expr, ...]
    start: int
    end: int


class Stmt:
    pass


@dataclass(frozen=True)
class AssignStmt(Stmt):
    name: str
    value: Expr
    start: int
    end: int


@dataclass(frozen=True)
class VarDeclStmt(Stmt):
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
class FuncDeclStmt(Stmt):
    name: str
    params: tuple[Param, ...]
    returnType: str
    body: tuple[Stmt, ...]
    start: int
    end: int


@dataclass(frozen=True)
class ReturnStmt(Stmt):
    value: Optional[Expr]
    start: int
    end: int


@dataclass(frozen=True)
class ExprStmt(Stmt):
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
class IfStmt(Stmt):
    condition: Expr
    ifBody: tuple[Stmt, ...]
    elifClauses: Optional[tuple[ElifClause, ...]]
    elseBody: Optional[tuple[Stmt, ...]]
    start: int
    end: int


@dataclass(frozen=True)
class WhileStmt(Stmt):
    condition: Expr
    body: tuple[Stmt, ...]
    onstop: Optional[tuple[Stmt, ...]]
    nostop: Optional[tuple[Stmt, ...]]
    start: int
    end: int


@dataclass(frozen=True)
class RepeatStmt(Stmt):
    ntimes: Expr
    body: tuple[Stmt, ...]
    onstop: Optional[tuple[Stmt, ...]]
    nostop: Optional[tuple[Stmt, ...]]
    start: int
    end: int


@dataclass(frozen=True)
class StopStmt(Stmt):
    start: int
    end: int


@dataclass(frozen=True)
class SkipStmt(Stmt):
    start: int
    end: int
