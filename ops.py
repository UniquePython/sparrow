import boolops
import intops
from values import BoolValue, IntValue


def add(a: IntValue | BoolValue, b: IntValue | BoolValue) -> IntValue | BoolValue:
    if isinstance(a, BoolValue):
        return boolops.add(a, b)
    else:
        return intops.add(a, b)


def sub(a: IntValue | BoolValue, b: IntValue | BoolValue) -> IntValue | BoolValue:
    if isinstance(a, BoolValue):
        return boolops.sub(a, b)
    else:
        return intops.sub(a, b)


def mul(a: IntValue | BoolValue, b: IntValue | BoolValue) -> IntValue:
    if isinstance(a, BoolValue):
        return boolops.mul(a, b)
    else:
        return intops.mul(a, b)


def div(a: IntValue | BoolValue, b: IntValue | BoolValue) -> IntValue:
    if isinstance(a, BoolValue):
        return boolops.div(a, b)
    else:
        return intops.div(a, b)


def mod(a: IntValue | BoolValue, b: IntValue | BoolValue) -> IntValue | BoolValue:
    if isinstance(a, BoolValue):
        return boolops.mod(a, b)
    else:
        return intops.mod(a, b)


def neg(x: IntValue) -> IntValue:
    return intops.neg(x)


def lnot(x: BoolValue) -> BoolValue:
    return boolops.lnot(x)


def eqeq(a: IntValue | BoolValue, b: IntValue | BoolValue) -> BoolValue:
    if isinstance(a, BoolValue):
        return boolops.eqeq(a, b)
    else:
        return intops.eqeq(a, b)


def neq(a: IntValue | BoolValue, b: IntValue | BoolValue) -> BoolValue:
    if isinstance(a, BoolValue):
        return boolops.neq(a, b)
    else:
        return intops.neq(a, b)


def lt(a: IntValue | BoolValue, b: IntValue | BoolValue) -> BoolValue:
    if isinstance(a, BoolValue):
        return boolops.lt(a, b)
    else:
        return intops.lt(a, b)


def le(a: IntValue | BoolValue, b: IntValue | BoolValue) -> BoolValue:
    if isinstance(a, BoolValue):
        return boolops.le(a, b)
    else:
        return intops.le(a, b)


def gt(a: IntValue | BoolValue, b: IntValue | BoolValue) -> BoolValue:
    if isinstance(a, BoolValue):
        return boolops.gt(a, b)
    else:
        return intops.gt(a, b)


def ge(a: IntValue | BoolValue, b: IntValue | BoolValue) -> BoolValue:
    if isinstance(a, BoolValue):
        return boolops.ge(a, b)
    else:
        return intops.ge(a, b)
