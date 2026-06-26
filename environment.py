from errors import SparrowRuntimeError
from values import Value


class Environment:
    def __init__(self):
        self.vars: dict[str, tuple[str, Value]] = {}

    def exists(self, name: str) -> bool:
        return name in self.vars

    def declare(self, name: str, type: str, value: Value, start: int, end: int) -> None:
        if self.exists(name):
            raise SparrowRuntimeError(
                f"Variable {name!r} is already declared in this scope", start, end
            )
        self.vars[name] = (type, value)

    def assign(self, name: str, value: Value, start: int, end: int) -> None:
        if not self.exists(name):
            raise SparrowRuntimeError(
                f"Cannot assign to undeclared variable {name!r}", start, end
            )
        self.vars[name] = (self.vars[name][0], value)

    def type(self, name: str, start: int, end: int) -> str:
        if self.exists(name):
            return self.vars[name][0]
        else:
            raise SparrowRuntimeError(
                f"Failed to access undeclared variable {name!r}", start, end
            )

    def value(self, name: str, start: int, end: int) -> Value:
        if self.exists(name):
            return self.vars[name][1]
        else:
            raise SparrowRuntimeError(
                f"Failed to access undeclared variable {name!r}", start, end
            )
