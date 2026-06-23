from errors import SparrowRuntimeError


class Environment:
    def __init__(self):
        self.vars: dict[str, int] = {}

    def define(self, name: str, value: int) -> None:
        self.vars[name] = value

    def get(self, name: str, start: int, end: int) -> int:
        if name in self.vars:
            return self.vars[name]
        else:
            raise SparrowRuntimeError(
                f"Failed to access undefined variable {name!r}", start, end
            )
