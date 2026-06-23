from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class IntValue:
    value: int


@dataclass(frozen=True)
class BoolValue:
    value: bool


Value = Union["IntValue", "BoolValue"]
