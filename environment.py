from errors import SparrowRuntimeError
from values import Value


class Environment:
    def __init__(self):
        self.vars: dict[str, Value] = {}

    def define(self, name: str, value: Value) -> None:
        self.vars[name] = value

    def get(self, name: str, start: int, end: int) -> Value:
        if name in self.vars:
            return self.vars[name]
        else:
            raise SparrowRuntimeError(
                f"Failed to access undefined variable {name!r}", start, end
            )
