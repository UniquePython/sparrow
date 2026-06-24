from ast_node import (
    AssignStmt,
    BinaryExpr,
    BinaryOp,
    Expr,
    ExprStmt,
    IdentifierExpr,
    NumberLiteral,
    Stmt,
    UnaryExpr,
    UnaryOp,
)
from environment import Environment
from errors import SparrowRuntimeError
from values import IntValue, Value


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


BINARY_OPS = {
    BinaryOp.ADD: add,
    BinaryOp.SUB: sub,
    BinaryOp.MUL: mul,
    BinaryOp.DIV: div,
    BinaryOp.MOD: mod,
}

UNARY_OPS = {
    UnaryOp.NEG: neg,
}


def evaluate(node: Expr, env: Environment) -> Value:
    match node:
        case NumberLiteral(value=value):
            return IntValue(value)

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


def execute(stmt: Stmt, env: Environment) -> Value:
    match stmt:
        case AssignStmt(name=name, value=value):
            result = evaluate(value, env)
            env.define(name, result)

            return result

        case ExprStmt(expr=expr):
            return evaluate(expr, env)

        case _:
            raise AssertionError(f"unhandled node type: {type(stmt).__name__}")
