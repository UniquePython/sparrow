from dataclasses import dataclass
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
