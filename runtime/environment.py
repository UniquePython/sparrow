from typing import Optional

from errors import SparrowRuntimeError
from runtime.values import Value


class Environment:
    def __init__(self, parent: Optional["Environment"] = None):
        self.parent = parent
        self.vars: dict[str, Value] = {}

    def exists(self, name: str) -> bool:
        if name in self.vars:
            return True
        if self.parent is not None:
            return self.parent.exists(name)
        return False

    def declare(self, name: str, value: Value, start: int, end: int) -> None:
        if name in self.vars:
            raise SparrowRuntimeError(
                f"Variable {name!r} is already declared in this scope",
                start,
                end,
            )

        self.vars[name] = (type, value)

    def assign(self, name: str, value: Value, start: int, end: int) -> None:
        if name in self.vars:
            self.vars[name] = value
        elif self.parent is not None:
            self.parent.assign(name, value, start, end)
        else:
            raise SparrowRuntimeError(
                f"Cannot assign to undeclared variable {name!r}", start, end
            )

    def value(self, name: str, start: int, end: int) -> Value:
        if name in self.vars:
            return self.vars[name]
        elif self.parent is not None:
            return self.parent.value(name, start, end)
        else:
            raise SparrowRuntimeError(
                f"Failed to access undeclared variable {name!r}", start, end
            )
