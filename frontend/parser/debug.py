from typing import Union

from frontend.ast import (
    AssignStmt,
    BinaryExpr,
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
    VarDeclStmt,
    WhileStmt,
)


def pretty(node: Union[Expr, Stmt], prefix="", is_root=True, is_last=True) -> None:
    if is_root:
        connector = ""
    elif is_last:
        connector = "└── "
    else:
        connector = "├── "

    child_prefix = prefix + ("" if is_root else ("    " if is_last else "│   "))

    match node:
        case NumberLiteral(value=value):
            print(prefix + connector + str(value))

        case BoolLiteral(value=value):
            boolStr = "true" if value else "false"
            print(prefix + connector + boolStr)

        case IdentifierExpr(name=name):
            print(prefix + connector + name)

        case FuncCallExpr(name=name, args=args):
            print(prefix + connector + f"CALL {name}")
            for i, arg in enumerate(args):
                pretty(arg, child_prefix, is_root=False, is_last=i == len(args) - 1)

        case UnaryExpr(operator=operator, operand=operand):
            print(prefix + connector + operator.name)
            pretty(
                operand,
                child_prefix,
                is_root=False,
                is_last=True,
            )

        case BinaryExpr(
            left=left,
            operator=operator,
            right=right,
        ):
            print(prefix + connector + operator.name)

            pretty(
                left,
                child_prefix,
                is_root=False,
                is_last=False,
            )

            pretty(
                right,
                child_prefix,
                is_root=False,
                is_last=True,
            )

        case ExprStmt(expr=expr):
            pretty(expr, prefix, is_root, is_last)

        case AssignStmt(name=name, value=value):
            print(prefix + connector + name)
            pretty(
                value,
                child_prefix,
                is_root=False,
                is_last=True,
            )

        case VarDeclStmt(type=type, name=name, value=value):
            print(prefix + connector + f"{type} {name}")
            pretty(value, child_prefix, is_root=False, is_last=True)

        case FuncDeclStmt(name=name, params=params, returnType=returnType, body=body):
            print(prefix + connector + f"FUNC {name} -> {returnType}")
            for i, param in enumerate(params):
                is_last_param = i == len(params) - 1 and len(body) == 0
                print(
                    child_prefix
                    + ("└── " if is_last_param else "├── ")
                    + f"PARAM {param.type} {param.name}"
                )
            for i, stmt in enumerate(body):
                pretty(stmt, child_prefix, is_root=False, is_last=i == len(body) - 1)

        case ReturnStmt(value=value):
            print(prefix + connector + "RETURN")
            if value is not None:
                pretty(value, child_prefix, is_root=False, is_last=True)

        case IfStmt(
            condition=condition,
            ifBody=ifBody,
            elifClauses=elifClauses,
            elseBody=elseBody,
        ):
            hasElif = len(elifClauses) > 0
            hasElse = elseBody is not None

            print(prefix + connector + "IF")
            pretty(
                condition,
                child_prefix,
                is_root=False,
                is_last=len(ifBody) == 0 and not hasElif and not hasElse,
            )

            for i, stmt in enumerate(ifBody):
                is_last_stmt = i == len(ifBody) - 1 and not hasElif and not hasElse
                pretty(stmt, child_prefix, is_root=False, is_last=is_last_stmt)

            for i, clause in enumerate(elifClauses):
                is_last_clause = i == len(elifClauses) - 1 and not hasElse

                print(child_prefix + ("└── " if is_last_clause else "├── ") + "ELIF")
                elif_prefix = child_prefix + ("    " if is_last_clause else "│   ")

                pretty(
                    clause.condition,
                    elif_prefix,
                    is_root=False,
                    is_last=len(clause.body) == 0,
                )

                for j, stmt in enumerate(clause.body):
                    pretty(
                        stmt,
                        elif_prefix,
                        is_root=False,
                        is_last=j == len(clause.body) - 1,
                    )

            if hasElse:
                print(child_prefix + "└── ELSE")
                else_prefix = child_prefix + "    "

                for i, stmt in enumerate(elseBody):
                    pretty(
                        stmt, else_prefix, is_root=False, is_last=i == len(elseBody) - 1
                    )

        case WhileStmt(condition=condition, body=body, onstop=onstop, nostop=nostop):
            hasOnstop = onstop is not None
            hasNostop = nostop is not None
            print(prefix + connector + "WHILE")
            pretty(
                condition,
                child_prefix,
                is_root=False,
                is_last=len(body) == 0 and not hasOnstop and not hasNostop,
            )
            for i, stmt in enumerate(body):
                pretty(
                    stmt,
                    child_prefix,
                    is_root=False,
                    is_last=i == len(body) - 1 and not hasOnstop and not hasNostop,
                )

            if hasOnstop:
                print(child_prefix + ("└── " if not hasNostop else "├── ") + "ONSTOP")
                onstop_prefix = child_prefix + ("    " if not hasNostop else "│   ")
                for i, stmt in enumerate(onstop):
                    pretty(
                        stmt, onstop_prefix, is_root=False, is_last=i == len(onstop) - 1
                    )

            if hasNostop:
                print(child_prefix + "└── NOSTOP")
                nostop_prefix = child_prefix + "    "
                for i, stmt in enumerate(nostop):
                    pretty(
                        stmt, nostop_prefix, is_root=False, is_last=i == len(nostop) - 1
                    )

        case RepeatStmt(ntimes=ntimes, body=body, onstop=onstop, nostop=nostop):
            hasOnstop = onstop is not None
            hasNostop = nostop is not None
            print(prefix + connector + "REPEAT")
            pretty(
                ntimes,
                child_prefix,
                is_root=False,
                is_last=len(body) == 0 and not hasOnstop and not hasNostop,
            )
            for i, stmt in enumerate(body):
                pretty(
                    stmt,
                    child_prefix,
                    is_root=False,
                    is_last=i == len(body) - 1 and not hasOnstop and not hasNostop,
                )

            if hasOnstop:
                print(child_prefix + ("└── " if not hasNostop else "├── ") + "ONSTOP")
                onstop_prefix = child_prefix + ("    " if not hasNostop else "│   ")
                for i, stmt in enumerate(onstop):
                    pretty(
                        stmt, onstop_prefix, is_root=False, is_last=i == len(onstop) - 1
                    )

            if hasNostop:
                print(child_prefix + "└── NOSTOP")
                nostop_prefix = child_prefix + "    "
                for i, stmt in enumerate(nostop):
                    pretty(
                        stmt, nostop_prefix, is_root=False, is_last=i == len(nostop) - 1
                    )

        case StopStmt():
            print(prefix + connector + "STOP")

        case SkipStmt():
            print(prefix + connector + "SKIP")

        case _:
            raise AssertionError(f"unhandled node type: {type(node).__name__}")
