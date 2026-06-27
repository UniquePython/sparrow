from runtime.values import BoolValue, IntValue


def add(a: IntValue, b: IntValue) -> IntValue:
    return IntValue(a.value + b.value)


def sub(a: IntValue, b: IntValue) -> IntValue:
    return IntValue(a.value - b.value)


def mul(a: IntValue, b: IntValue) -> IntValue:
    return IntValue(a.value * b.value)


def div(a: IntValue, b: IntValue) -> IntValue:
    return IntValue(int(a.value / b.value))


def mod(a: IntValue, b: IntValue) -> IntValue:
    return IntValue(a.value - div(a, b).value * b.value)


def neg(x: IntValue) -> IntValue:
    return IntValue(-x.value)


def eqeq(a: IntValue, b: IntValue) -> BoolValue:
    return BoolValue(a.value == b.value)


def neq(a: IntValue, b: IntValue) -> BoolValue:
    return BoolValue(a.value != b.value)


def lt(a: IntValue, b: IntValue) -> BoolValue:
    return BoolValue(a.value < b.value)


def le(a: IntValue, b: IntValue) -> BoolValue:
    return BoolValue(a.value <= b.value)


def gt(a: IntValue, b: IntValue) -> BoolValue:
    return BoolValue(a.value > b.value)


def ge(a: IntValue, b: IntValue) -> BoolValue:
    return BoolValue(a.value >= b.value)
