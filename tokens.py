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
    LBRACE = auto()
    RBRACE = auto()
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
    IF = auto()
    UNLESS = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    UNTIL = auto()
    FOREVER = auto()
    REPEAT = auto()
    STOP = auto()
    SKIP = auto()
    ONSTOP = auto()
    NOSTOP = auto()
    FUNCTION = auto()
    RETURN = auto()
    ARROW = auto()
    COMMA = auto()
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
    "{": TokenKind.LBRACE,
    "}": TokenKind.RBRACE,
    ";": TokenKind.SEMICOLON,
    ",": TokenKind.COMMA,
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
    "->": TokenKind.ARROW,
}

KEYWORDS_TO_TOKENKIND: dict[str, TokenKind] = {
    "true": TokenKind.TRUE,
    "false": TokenKind.FALSE,
    "if": TokenKind.IF,
    "unless": TokenKind.UNLESS,
    "elif": TokenKind.ELIF,
    "else": TokenKind.ELSE,
    "while": TokenKind.WHILE,
    "until": TokenKind.UNTIL,
    "forever": TokenKind.FOREVER,
    "repeat": TokenKind.REPEAT,
    "stop": TokenKind.STOP,
    "skip": TokenKind.SKIP,
    "onstop": TokenKind.ONSTOP,
    "nostop": TokenKind.NOSTOP,
    "function": TokenKind.FUNCTION,
    "return": TokenKind.RETURN,
}

TOKEN_DISPLAY = {
    TokenKind.PLUS: "+",
    TokenKind.MINUS: "-",
    TokenKind.ASTERISK: "*",
    TokenKind.FSLASH: "/",
    TokenKind.PERCENT: "%",
    TokenKind.LPAREN: "(",
    TokenKind.RPAREN: ")",
    TokenKind.LBRACE: "{",
    TokenKind.RBRACE: "}",
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
    TokenKind.IF: "if",
    TokenKind.UNLESS: "unless",
    TokenKind.ELIF: "elif",
    TokenKind.ELSE: "else",
    TokenKind.WHILE: "while",
    TokenKind.FOREVER: "forever",
    TokenKind.UNTIL: "until",
    TokenKind.REPEAT: "repeat",
    TokenKind.STOP: "stop",
    TokenKind.SKIP: "skip",
    TokenKind.ONSTOP: "onstop",
    TokenKind.NOSTOP: "nostop",
    TokenKind.FUNCTION: "function",
    TokenKind.RETURN: "return",
    TokenKind.ARROW: "->",
    TokenKind.COMMA: ",",
    TokenKind.EOF: "end of file",
}
