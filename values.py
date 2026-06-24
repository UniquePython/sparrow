from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class IntValue:
    value: int

    def __repr__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True)
class BooleanValue:
    value: bool

    def __repr__(self) -> str:
        return "true" if self.value else "false"


Value = Union["IntValue", "BooleanValue"]
