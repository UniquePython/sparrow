from runtime.values import BoolValue

BOOL_TO_INT: dict[bool, int] = {True: 1, False: 0}
INT_TO_BOOL: dict[int, bool] = {v: k for k, v in BOOL_TO_INT.items()}


def add(a: BoolValue, b: BoolValue) -> BoolValue:
    aInt = BOOL_TO_INT[a.value]
    bInt = BOOL_TO_INT[b.value]
    return BoolValue(INT_TO_BOOL[(aInt + bInt) % 2])


def sub(a: BoolValue, b: BoolValue) -> BoolValue:
    aInt = BOOL_TO_INT[a.value]
    bInt = BOOL_TO_INT[b.value]
    return BoolValue(INT_TO_BOOL[(aInt - bInt) % 2])


def mul(a: BoolValue, b: BoolValue) -> BoolValue:
    aInt = BOOL_TO_INT[a.value]
    bInt = BOOL_TO_INT[b.value]
    return BoolValue(INT_TO_BOOL[(aInt * bInt) % 2])


# b is guaranteed true here, division is identity
def div(a: BoolValue, b: BoolValue) -> BoolValue:
    return a


def mod(a: BoolValue, b: BoolValue) -> BoolValue:
    aInt = BOOL_TO_INT[a.value]
    bInt = BOOL_TO_INT[b.value]
    divInt = BOOL_TO_INT[div(a, b).value]
    return BoolValue(INT_TO_BOOL[(aInt - divInt * bInt) % 2])


def lnot(x: BoolValue) -> BoolValue:
    return BoolValue(not x.value)


def eqeq(a: BoolValue, b: BoolValue) -> BoolValue:
    aInt = BOOL_TO_INT[a.value]
    bInt = BOOL_TO_INT[b.value]
    return BoolValue(aInt == bInt)


def neq(a: BoolValue, b: BoolValue) -> BoolValue:
    aInt = BOOL_TO_INT[a.value]
    bInt = BOOL_TO_INT[b.value]
    return BoolValue(aInt != bInt)


def lt(a: BoolValue, b: BoolValue) -> BoolValue:
    aInt = BOOL_TO_INT[a.value]
    bInt = BOOL_TO_INT[b.value]
    return BoolValue(aInt < bInt)


def le(a: BoolValue, b: BoolValue) -> BoolValue:
    aInt = BOOL_TO_INT[a.value]
    bInt = BOOL_TO_INT[b.value]
    return BoolValue(aInt <= bInt)


def gt(a: BoolValue, b: BoolValue) -> BoolValue:
    aInt = BOOL_TO_INT[a.value]
    bInt = BOOL_TO_INT[b.value]
    return BoolValue(aInt > bInt)


def ge(a: BoolValue, b: BoolValue) -> BoolValue:
    aInt = BOOL_TO_INT[a.value]
    bInt = BOOL_TO_INT[b.value]
    return BoolValue(aInt >= bInt)
