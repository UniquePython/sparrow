from ast_node import BinaryExpr, NumberLiteral
from tokens import TokenKind


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        raise ZeroDivisionError("Found illegal divisor 0")
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
        op = BINARY_OPS[node.operator]
        return op(left, right)
