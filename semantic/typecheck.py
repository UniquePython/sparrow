from typing import Optional

from errors import SparrowTypeError
from frontend.ast import (
    AssignStmt,
    BinaryExpr,
    BinaryOp,
    BoolLiteral,
    Expr,
    ExprStmt,
    FuncCallExpr,
    FuncDeclStmt,
    IdentifierExpr,
    IfStmt,
    NumberLiteral,
    RepeatStmt,
    ReturnStmt,
    SkipStmt,
    Stmt,
    StopStmt,
    UnaryExpr,
    UnaryOp,
    VarDeclStmt,
    WhileStmt,
)
from semantic.type_environment import TypeEnvironment
from semantic.type_registry import Registry
from semantic.types_ import Bool, FuncType, Int, Nothing, Type

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
                return Int if lhsType == Int else Bool
            elif operator in BINARY_COMPARISON_OPS:
                return Bool
            else:
                raise AssertionError(f"unhandled operator type {operator.name}")

        case UnaryExpr(operator=operator, operand=operand):
            operandType = checkExpr(operand, env)

            if operator in UNARY_ARITHMETIC_OPS:
                if operandType != Int:
                    raise SparrowTypeError(
                        f"Expected 'Int', found {operandType!r} instead",
                        operand.start,
                        operand.end,
                    )
                return Int
            elif operator in UNARY_LOGICAL_OPS:
                if operandType != Bool:
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

            if not isinstance(funcType, FuncType):
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


def checkBlock(
    block: tuple[Stmt, ...],
    parentEnv: TypeEnvironment,
    expectedReturnType: Optional[Type],
    insideLoop: bool,
) -> None:
    blockEnv = TypeEnvironment(parent=parentEnv)
    for stmt in block:
        checkStmt(stmt, blockEnv, insideLoop, expectedReturnType)


def checkCondition(condition: Expr, expectedType: Type, env: TypeEnvironment) -> None:
    conditionType = checkExpr(condition, env)
    if conditionType != expectedType:
        raise SparrowTypeError(
            f"Condition must evaluate to a '{expectedType}'",
            condition.start,
            condition.end,
        )


def checkStmt(
    stmt: Stmt,
    env: TypeEnvironment,
    insideLoop: bool,
    expectedReturnType: Optional[Type] = None,
) -> None:
    match stmt:
        case AssignStmt(name=name, value=value, start=start, end=end):
            existingType = env.type(name, start, end)
            newValueType = checkExpr(value, env)

            if existingType != newValueType:
                raise SparrowTypeError(
                    f"Expected variable '{name}' to be assigned with type '{existingType}' but found type '{newValueType}' instead",
                    value.start,
                    value.end,
                )

        case VarDeclStmt(type=type, name=name, value=value, start=start, end=end):
            declaredType = Registry.resolve(type, start, end)

            if declaredType == Nothing:
                raise SparrowTypeError(
                    "Cannot declare a variable of type 'Nothing'", start, end
                )

            valueType = checkExpr(value, env)

            if declaredType != valueType:
                raise SparrowTypeError(
                    f"Expected variable '{name}' to be initialized with type '{declaredType}' but found type '{valueType}' instead",
                    value.start,
                    value.end,
                )

            env.declare(name, declaredType, start, end)

        case FuncDeclStmt(
            name=name,
            params=params,
            returnType=returnType,
            body=body,
            start=start,
            end=end,
        ):

            returnTypeResolved = Registry.resolve(returnType, start, end)
            paramTypes = []
            for param in params:
                paramType = Registry.resolve(param.type, param.start, param.end)
                paramTypes.append(paramType)

            funcType = FuncType(paramTypes, returnTypeResolved)

            env.declare(name, funcType, start, end)

            funcEnv = TypeEnvironment(parent=env)

            for i in range(len(params)):
                param = params[i]
                paramType = paramTypes[i]
                funcEnv.declare(param.name, paramType, param.start, param.end)

            for stmt in body:
                checkStmt(stmt, funcEnv, False, returnTypeResolved)

        case ReturnStmt(value=value, start=start, end=end):
            if expectedReturnType is None:
                raise SparrowTypeError(
                    "Found illegal 'return' outside a function", start, end
                )

            if expectedReturnType == Nothing and value is not None:
                valueType = checkExpr(value, env)
                raise SparrowTypeError(
                    f"Expected to return 'Nothing' but returned '{valueType}' instead",
                    start,
                    end,
                )

            if expectedReturnType != Nothing:
                if value is None:
                    raise SparrowTypeError(
                        f"Expected to return '{expectedReturnType}' but returned 'Nothing' instead",
                        start,
                        end,
                    )

                valueType = checkExpr(value, env)
                if expectedReturnType != valueType:
                    raise SparrowTypeError(
                        f"Expected to return {expectedReturnType} but returned '{valueType}' instead",
                        start,
                        end,
                    )

        case ExprStmt(expr=expr):
            checkExpr(expr, env)

        case IfStmt(
            condition=condition,
            ifBody=ifBody,
            elifClauses=elifClauses,
            elseBody=elseBody,
        ):
            checkCondition(condition, Bool, env)
            checkBlock(ifBody, env, expectedReturnType, insideLoop)

            for elifClause in elifClauses:
                checkCondition(elifClause.condition, Bool, env)
                checkBlock(elifClause.body, env, expectedReturnType, insideLoop)

            if elseBody is not None:
                checkBlock(elseBody, env, expectedReturnType, insideLoop)

        case WhileStmt(
            condition=condition, body=whileBody, onstop=onstop, nostop=nostop
        ):
            checkCondition(condition, Bool, env)
            checkBlock(whileBody, env, expectedReturnType, insideLoop=True)

            if onstop is not None:
                checkBlock(onstop, env, expectedReturnType, insideLoop=False)

            if nostop is not None:
                checkBlock(nostop, env, expectedReturnType, insideLoop=False)

        case RepeatStmt(ntimes=ntimes, body=repeatBody, onstop=onstop, nostop=nostop):
            checkCondition(ntimes, Int, env)
            checkBlock(repeatBody, env, expectedReturnType, insideLoop=True)

            if onstop is not None:
                checkBlock(onstop, env, expectedReturnType, insideLoop=False)

            if nostop is not None:
                checkBlock(nostop, env, expectedReturnType, insideLoop=False)

        case StopStmt(start=start, end=end):
            if not insideLoop:
                raise SparrowTypeError(
                    "Stop statement cannot be used outside a loop", start, end
                )

        case SkipStmt(start=start, end=end):
            if not insideLoop:
                raise SparrowTypeError(
                    "Skip statement cannot be used outside a loop", start, end
                )

        case _:
            raise AssertionError(f"unhandled stmt type: {type(stmt).__name__}")
