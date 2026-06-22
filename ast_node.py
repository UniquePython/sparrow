from dataclasses import dataclass
from enum import Enum, auto
from typing import Union


class BinaryOp(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()


@dataclass(frozen=True)
class NumberLiteral:
    value: int

    start: int
    end: int

    def __repr__(self) -> str:
        return f"NumberLiteral => {self.value}"


Expr = Union["NumberLiteral", "BinaryExpr"]


@dataclass(frozen=True)
class BinaryExpr:
    operator: BinaryOp
    left: Expr
    right: Expr

    start: int
    end: int

    def __repr__(self) -> str:
        return f"BinaryExpr => [{self.left}]->[{self.operator}]<-[{self.right}]"


if __name__ == "__main__":
    from tokens import TokenKind

    print(
        BinaryExpr(
            TokenKind.PLUS,
            NumberLiteral(1, 1, 2),
            BinaryExpr(TokenKind.ASTERISK, NumberLiteral(2), NumberLiteral(3), 1, 2),
            1,
            2,
        )
    )
