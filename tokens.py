from enum import Enum, auto


class TokenKind(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    ASTERISK = auto()
    FSLASH = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()


class Token:
    def __init__(self, kind, value, start, end):
        self.kind = kind
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Token({self.kind}, {self.value!r})"


SINGLE_CHAR_TOKENS = {
    "+": TokenKind.PLUS,
    "-": TokenKind.MINUS,
    "*": TokenKind.ASTERISK,
    "/": TokenKind.FSLASH,
    "(": TokenKind.LPAREN,
    ")": TokenKind.RPAREN,
}
