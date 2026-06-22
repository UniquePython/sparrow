from dataclasses import dataclass
from typing import Union

from tokens import TokenKind


@dataclass(frozen=True)
class NumberLiteral:
    value: int

    start: int
    end: int

    def __repr__(self) -> str:
        return f"NumberLiteral => {self.value}"


@dataclass(frozen=True)
class BinaryExpr:
    operator: TokenKind
    left: Union[NumberLiteral, "BinaryExpr"]
    right: Union[NumberLiteral, "BinaryExpr"]

    start: int
    end: int

    def __repr__(self) -> str:
        return f"BinaryExpr => [{self.left}]->[{self.operator}]<-[{self.right}]"


if __name__ == "__main__":
    print(
        BinaryExpr(
            TokenKind.PLUS,
            NumberLiteral(1),
            BinaryExpr(TokenKind.ASTERISK, NumberLiteral(2), NumberLiteral(3)),
        )
    )
