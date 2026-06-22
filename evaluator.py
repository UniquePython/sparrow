from ast_node import BinaryExpr, NumberLiteral
from errors import SparrowRuntimeError
from tokens import TokenKind


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return int(a / b)


BINARY_OPS = {
    TokenKind.PLUS: add,
    TokenKind.MINUS: sub,
    TokenKind.ASTERISK: mul,
    TokenKind.FSLASH: div,
}


def evaluate(node):
    if isinstance(node, NumberLiteral):
        return node.value
    elif isinstance(node, BinaryExpr):
        left = evaluate(node.left)
        right = evaluate(node.right)

        if node.operator == TokenKind.FSLASH and right == 0:
            raise SparrowRuntimeError(
                "Found illegal divisor 0", node.right.start, node.right.end
            )

        op = BINARY_OPS[node.operator]
        return op(left, right)
