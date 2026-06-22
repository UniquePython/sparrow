from ast_node import BinaryExpr, BinaryOp, Expr, NumberLiteral, UnaryExpr, UnaryOp
from errors import SparrowRuntimeError


def add(a: int, b: int) -> int:
    return a + b


def sub(a: int, b: int) -> int:
    return a - b


def mul(a: int, b: int) -> int:
    return a * b


def div(a: int, b: int) -> int:
    return int(a / b)


def neg(x: int) -> int:
    return -x


BINARY_OPS = {
    BinaryOp.ADD: add,
    BinaryOp.SUB: sub,
    BinaryOp.MUL: mul,
    BinaryOp.DIV: div,
}

UNARY_OPS = {
    UnaryOp.NEG: neg,
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

    elif isinstance(node, UnaryExpr):
        operand = evaluate(node.operand)
        op = UNARY_OPS[node.operator]
        return op(operand)
