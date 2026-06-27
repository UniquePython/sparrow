from errors import SparrowTypeError
from semantic.types_ import Bool, Int, Nothing, Type


class TypeRegistry:
    def __init__(self):
        self.symbols: dict[str, Type] = {
            "Int": Int,
            "Bool": Bool,
            "Nothing": Nothing,
        }

    def resolve(self, name: str, start: int, end: int) -> Type:
        if name in self.symbols:
            return self.symbols[name]
        else:
            raise SparrowTypeError(f"Unknown type {name}", start, end)


Registry = TypeRegistry()
