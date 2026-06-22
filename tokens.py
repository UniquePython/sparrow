from enum import Enum, auto
from typing import Optional, Union


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
    def __init__(
        self, kind: TokenKind, value: Optional[Union[str, int]], start: int, end: int
    ):
        self.kind = kind
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"Token => {self.kind}<{self.value!r}> spans [{self.start}, {self.end})"


SINGLE_CHAR_TOKENS = {
    "+": TokenKind.PLUS,
    "-": TokenKind.MINUS,
    "*": TokenKind.ASTERISK,
    "/": TokenKind.FSLASH,
    "(": TokenKind.LPAREN,
    ")": TokenKind.RPAREN,
}

TOKEN_DISPLAY = {
    TokenKind.PLUS: "+",
    TokenKind.MINUS: "-",
    TokenKind.ASTERISK: "*",
    TokenKind.FSLASH: "/",
    TokenKind.LPAREN: "(",
    TokenKind.RPAREN: ")",
    TokenKind.NUMBER: "number",
    TokenKind.EOF: "end of file",
}
