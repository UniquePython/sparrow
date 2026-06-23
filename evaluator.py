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


def add(a: int, b: int) -> int:
    return a + b


def sub(a: int, b: int) -> int:
    return a - b


def mul(a: int, b: int) -> int:
    return a * b


def div(a: int, b: int) -> int:
    return int(a / b)


def mod(a: int, b: int) -> int:
    return a - div(a, b) * b


def neg(x: int) -> int:
    return -x


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


def evaluate(node: Expr, env: Environment) -> int:
    if isinstance(node, NumberLiteral):
        return node.value

    elif isinstance(node, BinaryExpr):
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)

        if node.operator in {BinaryOp.DIV, BinaryOp.MOD} and right == 0:
            raise SparrowRuntimeError(
                "Cannot divide by 0", node.right.start, node.right.end
            )

        op = BINARY_OPS[node.operator]
        return op(left, right)

    elif isinstance(node, UnaryExpr):
        operand = evaluate(node.operand, env)
        op = UNARY_OPS[node.operator]
        return op(operand)

    elif isinstance(node, IdentifierExpr):
        return env.get(node.name, node.start, node.end)

    else:
        raise AssertionError(f"unhandled node type: {type(node).__name__}")


def execute(stmt: Stmt, env: Environment) -> None:
    if isinstance(stmt, AssignStmt):
        value = evaluate(stmt.value, env)
        env.define(stmt.name, value)

    elif isinstance(stmt, ExprStmt):
        evaluate(stmt.expr, env)

    else:
        raise AssertionError(f"unhandled node type: {type(stmt).__name__}")
