from dataclasses import dataclass


class Type:
    pass


@dataclass(frozen=True)
class IntType(Type):
    def __repr__(self) -> str:
        return "Int"


@dataclass(frozen=True)
class BoolType(Type):
    def __repr__(self) -> str:
        return "Bool"


@dataclass(frozen=True)
class NothingType(Type):
    def __repr__(self) -> str:
        return "Nothing"


@dataclass(frozen=True)
class FuncType(Type):
    paramTypes: tuple[Type, ...]
    returnType: Type

    def __repr__(self) -> str:
        params = ", ".join(str(p) for p in self.paramTypes)
        return f"({params}) -> {self.returnType}"


Int = IntType()
Bool = BoolType()
Nothing = NothingType()
