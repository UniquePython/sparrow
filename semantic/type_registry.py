from errors import SparrowTypeError, suggestClosest
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
            suggestion = suggestClosest(name, list(self.symbols.keys()))
            extra = f". {suggestion}" if suggestion is not None else ""
            raise SparrowTypeError(f"Unknown type {name!r}{extra}", start, end)


Registry = TypeRegistry()
