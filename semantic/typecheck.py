from errors import SparrowTypeError
from frontend.ast import (
    BinaryExpr,
    BinaryOp,
    BoolLiteral,
    Expr,
    FuncCallExpr,
    IdentifierExpr,
    NumberLiteral,
    Stmt,
    UnaryExpr,
    UnaryOp,
)
from semantic.type_environment import TypeEnvironment
from semantic.types_ import Bool, FuncType, Int, Type

BINARY_ARITHMETIC_OPS = {
    BinaryOp.ADD,
    BinaryOp.SUB,
    BinaryOp.MUL,
    BinaryOp.DIV,
    BinaryOp.MOD,
}
BINARY_COMPARISON_OPS = {
    BinaryOp.EQEQ,
    BinaryOp.NEQ,
    BinaryOp.LT,
    BinaryOp.LE,
    BinaryOp.GT,
    BinaryOp.GE,
}
UNARY_ARITHMETIC_OPS = {UnaryOp.NEG}
UNARY_LOGICAL_OPS = {UnaryOp.NOT}


def checkExpr(expr: Expr, env: TypeEnvironment) -> Type:
    match expr:
        case NumberLiteral():
            return Int

        case BoolLiteral():
            return Bool

        case BinaryExpr(left=left, operator=operator, right=right):
            lhsType = checkExpr(left, env)
            rhsType = checkExpr(right, env)

            if lhsType not in {Int, Bool}:
                raise SparrowTypeError(
                    f"Expected 'Int/Bool', found {lhsType!r} instead",
                    left.start,
                    left.end,
                )

            if rhsType not in {Int, Bool}:
                raise SparrowTypeError(
                    f"Expected 'Int/Bool', found {rhsType!r} instead",
                    right.start,
                    right.end,
                )

            if lhsType != rhsType:
                raise SparrowTypeError(
                    f"Cannot perform binary operation between {lhsType!r} and {rhsType!r}",
                    left.start,
                    right.end,
                )

            if operator in BINARY_ARITHMETIC_OPS:
                return Int if lhsType is Int else Bool
            elif operator in BINARY_COMPARISON_OPS:
                return Bool
            else:
                raise AssertionError(f"unhandled operator type {operator.name}")

        case UnaryExpr(operator=operator, operand=operand):
            operandType = checkExpr(operand, env)

            if operator in UNARY_ARITHMETIC_OPS:
                if operandType is not Int:
                    raise SparrowTypeError(
                        f"Expected 'Int', found {operandType!r} instead",
                        operand.start,
                        operand.end,
                    )
                return Int
            elif operator in UNARY_LOGICAL_OPS:
                if operandType is not Bool:
                    raise SparrowTypeError(
                        f"Expected 'Bool', found {operandType!r} instead",
                        operand.start,
                        operand.end,
                    )
                return Bool
            else:
                raise AssertionError(f"unhandled operator type {operator.name}")

        case IdentifierExpr(name=name, start=start, end=end):
            return env.type(name, start, end)

        case FuncCallExpr(name=name, args=args, start=start, end=end):
            funcType = env.type(name, start, end)

            if type(funcType) is not FuncType:
                raise SparrowTypeError(
                    f"Cannot call {env.symbolStr(funcType).lower()} {name!r} like a function",
                    start,
                    end,
                )

            argsLen = len(args)
            paramsLen = len(funcType.paramTypes)

            if paramsLen != argsLen:
                raise SparrowTypeError(
                    f"Function {name!r} expects {paramsLen} parameters but {argsLen} arguments were provided",
                    start=start,
                    end=end,
                )

            for i, (paramType, arg) in enumerate(zip(funcType.paramTypes, args)):
                argType = checkExpr(arg, env)

                if argType != paramType:
                    raise SparrowTypeError(
                        f"{env.symbolStr(funcType)} {name!r} expects parameter of type {paramType!r} at position {i+1} but received {argType!r} instead",
                        arg.start,
                        arg.end,
                    )

            return funcType.returnType

        case _:
            raise AssertionError(f"unhandled expr type: {type(expr).__name__}")


def checkStmt(stmt: Stmt, env: TypeEnvironment) -> None:
    pass
