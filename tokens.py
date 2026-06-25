from dataclasses import dataclass
from enum import Enum, auto


class TokenKind(Enum):
    PLUS = auto()
    MINUS = auto()
    ASTERISK = auto()
    FSLASH = auto()
    PERCENT = auto()
    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    EQ = auto()
    EQEQ = auto()
    NOT = auto()
    NEQ = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    TRUE = auto()
    FALSE = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    value: str | int | None
    start: int
    end: int

    def __repr__(self) -> str:
        return (
            f"Token => {self.kind}" f"<{self.value!r}> spans [{self.start}, {self.end})"
        )


SINGLE_CHAR_TOKENS = {
    "+": TokenKind.PLUS,
    "-": TokenKind.MINUS,
    "*": TokenKind.ASTERISK,
    "/": TokenKind.FSLASH,
    "%": TokenKind.PERCENT,
    "(": TokenKind.LPAREN,
    ")": TokenKind.RPAREN,
    ";": TokenKind.SEMICOLON,
}

MULTI_CHAR_TOKENS = {
    "=": TokenKind.EQ,
    "==": TokenKind.EQEQ,
    "<": TokenKind.LT,
    "<=": TokenKind.LE,
    ">": TokenKind.GT,
    ">=": TokenKind.GE,
    "!": TokenKind.NOT,
    "!=": TokenKind.NEQ,
}

TOKEN_DISPLAY = {
    TokenKind.PLUS: "+",
    TokenKind.MINUS: "-",
    TokenKind.ASTERISK: "*",
    TokenKind.FSLASH: "/",
    TokenKind.PERCENT: "%",
    TokenKind.LPAREN: "(",
    TokenKind.RPAREN: ")",
    TokenKind.SEMICOLON: ";",
    TokenKind.EQ: "=",
    TokenKind.LT: "<",
    TokenKind.GT: ">",
    TokenKind.EQEQ: "==",
    TokenKind.NOT: "!",
    TokenKind.NEQ: "!=",
    TokenKind.LE: "<=",
    TokenKind.GE: ">=",
    TokenKind.NUMBER: "number",
    TokenKind.IDENTIFIER: "identifier",
    TokenKind.TRUE: "true",
    TokenKind.FALSE: "false",
    TokenKind.EOF: "end of file",
}
