from dataclasses import dataclass
from typing import TYPE_CHECKING

from frontend.ast import Param, Stmt

if TYPE_CHECKING:
    from runtime.environment import Environment


class Value:
    pass


@dataclass(frozen=True)
class IntValue(Value):
    value: int

    def __repr__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True)
class BoolValue(Value):
    value: bool

    def __repr__(self) -> str:
        return "true" if self.value else "false"


@dataclass(frozen=True)
class FuncValue(Value):
    params: tuple[Param, ...]
    returnType: str
    body: tuple[Stmt, ...]
    closure: "Environment"

    def __repr__(self) -> str:
        params = ", ".join(f"{p.type} {p.name}" for p in self.params)
        return f"Function ({params}) -> {self.returnType}"
