from typing import Optional

from ast_node import (
    AssignStmt,
    BinaryExpr,
    BinaryOp,
    BooleanLiteral,
    Expr,
    ExprStmt,
    IdentifierExpr,
    IfStmt,
    NumberLiteral,
    Stmt,
    UnaryExpr,
    UnaryOp,
)
from environment import Environment
from errors import SparrowRuntimeError
from values import BooleanValue, IntValue, Value


def add(a: IntValue, b: IntValue) -> IntValue:
    return IntValue(a.value + b.value)


def sub(a: IntValue, b: IntValue) -> IntValue:
    return IntValue(a.value - b.value)


def mul(a: IntValue, b: IntValue) -> IntValue:
    return IntValue(a.value * b.value)


def div(a: IntValue, b: IntValue) -> IntValue:
    return IntValue(int(a.value / b.value))


def mod(a: IntValue, b: IntValue) -> IntValue:
    return IntValue(a.value - div(a, b).value * b.value)


def neg(x: IntValue) -> IntValue:
    return IntValue(-x.value)


def lnot(x: BooleanValue) -> BooleanValue:
    return BooleanValue(not x.value)


def eqeq(a: IntValue, b: IntValue) -> BooleanValue:
    return BooleanValue(a.value == b.value)


def neq(a: IntValue, b: IntValue) -> BooleanValue:
    return BooleanValue(a.value != b.value)


def lt(a: IntValue, b: IntValue) -> BooleanValue:
    return BooleanValue(a.value < b.value)


def le(a: IntValue, b: IntValue) -> BooleanValue:
    return BooleanValue(a.value <= b.value)


def gt(a: IntValue, b: IntValue) -> BooleanValue:
    return BooleanValue(a.value > b.value)


def ge(a: IntValue, b: IntValue) -> BooleanValue:
    return BooleanValue(a.value >= b.value)


BINARY_OPS = {
    BinaryOp.ADD: add,
    BinaryOp.SUB: sub,
    BinaryOp.MUL: mul,
    BinaryOp.DIV: div,
    BinaryOp.MOD: mod,
    BinaryOp.EQEQ: eqeq,
    BinaryOp.NEQ: neq,
    BinaryOp.LT: lt,
    BinaryOp.LE: le,
    BinaryOp.GT: gt,
    BinaryOp.GE: ge,
}

UNARY_OPS = {
    UnaryOp.NEG: neg,
    UnaryOp.NOT: lnot,
}


def evaluate(node: Expr, env: Environment) -> Value:
    match node:
        case NumberLiteral(value=value):
            return IntValue(value)

        case BooleanLiteral(value=value):
            return BooleanValue(value)

        case BinaryExpr(left=left, operator=operator, right=right):
            lhs = evaluate(left, env)
            rhs = evaluate(right, env)

            if operator in {BinaryOp.DIV, BinaryOp.MOD} and rhs.value == 0:
                raise SparrowRuntimeError(
                    "Cannot divide by 0",
                    right.start,
                    right.end,
                )

            return BINARY_OPS[operator](lhs, rhs)

        case UnaryExpr(operator=operator, operand=operand):
            value = evaluate(operand, env)
            return UNARY_OPS[operator](value)

        case IdentifierExpr(name=name, start=start, end=end):
            return env.get(name, start, end)

        case _:
            raise AssertionError(f"unhandled node type: {type(node).__name__}")


def execute(stmt: Stmt, env: Environment) -> Optional[Value]:
    match stmt:
        case AssignStmt(name=name, value=value):
            result = evaluate(value, env)
            env.define(name, result)

            return result

        case ExprStmt(expr=expr):
            return evaluate(expr, env)

        case IfStmt(
            condition=condition,
            ifBody=ifBody,
            elifClauses=elifClauses,
            elseBody=elseBody,
        ):
            ifCond = evaluate(condition, env)

            if ifCond.value:
                for ifStmt in ifBody:
                    execute(ifStmt, env)
            else:
                for elifClause in elifClauses:
                    elifCond = evaluate(elifClause.condition, env)
                    if elifCond.value:
                        for elifStmt in elifClause.body:
                            execute(elifStmt, env)
                        break

                else:
                    if elseBody is not None:
                        for elseStmt in elseBody:
                            execute(elseStmt, env)

        case _:
            raise AssertionError(f"unhandled node type: {type(stmt).__name__}")
