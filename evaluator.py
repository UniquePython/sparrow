from ast_node import BinaryExpr, BinaryOp, Expr, NumberLiteral
from errors import SparrowRuntimeError


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return int(a / b)


BINARY_OPS = {
    BinaryOp.ADD: add,
    BinaryOp.SUB: sub,
    BinaryOp.MUL: mul,
    BinaryOp.DIV: div,
}


def evaluate(node: Expr) -> int:
    if isinstance(node, NumberLiteral):
        return node.value
    elif isinstance(node, BinaryExpr):
        left = evaluate(node.left)
        right = evaluate(node.right)

        if node.operator == BinaryOp.DIV and right == 0:
            raise SparrowRuntimeError(
                "Cannot divide by 0", node.right.start, node.right.end
            )

        op = BINARY_OPS[node.operator]
        return op(left, right)
