from typing import Union

from ast_node import (
    AssignStmt,
    BinaryExpr,
    BinaryOp,
    BoolLiteral,
    ElifClause,
    Expr,
    ExprStmt,
    FuncCallExpr,
    FuncDeclStmt,
    IdentifierExpr,
    IfStmt,
    NumberLiteral,
    Param,
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
from errors import SparrowParseError
from tokens import TOKEN_DISPLAY, Token, TokenKind

INFIX_BINDING_POWER = {
    TokenKind.EQEQ: 1,
    TokenKind.NEQ: 1,
    TokenKind.LT: 1,
    TokenKind.LE: 1,
    TokenKind.GT: 1,
    TokenKind.GE: 1,
    TokenKind.PLUS: 3,
    TokenKind.MINUS: 3,
    TokenKind.ASTERISK: 5,
    TokenKind.FSLASH: 5,
    TokenKind.PERCENT: 5,
}

PREFIX_BINDING_POWER = {TokenKind.MINUS: 7, TokenKind.NOT: 7}

TOKEN_TO_BINARY_OP = {
    TokenKind.PLUS: BinaryOp.ADD,
    TokenKind.MINUS: BinaryOp.SUB,
    TokenKind.ASTERISK: BinaryOp.MUL,
    TokenKind.FSLASH: BinaryOp.DIV,
    TokenKind.PERCENT: BinaryOp.MOD,
    TokenKind.EQEQ: BinaryOp.EQEQ,
    TokenKind.NEQ: BinaryOp.NEQ,
    TokenKind.LT: BinaryOp.LT,
    TokenKind.LE: BinaryOp.LE,
    TokenKind.GT: BinaryOp.GT,
    TokenKind.GE: BinaryOp.GE,
}

TOKEN_TO_UNARY_OP = {
    TokenKind.MINUS: UnaryOp.NEG,
    TokenKind.NOT: UnaryOp.NOT,
}


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def peekToken(self, offset: int = 0) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF token is always last
        return self.tokens[pos]

    def peekTokenKind(self, offset: int = 0) -> TokenKind:
        return self.peekToken(offset).kind

    def advance(self) -> Token:
        tok = self.peekToken()
        self.pos += 1
        return tok

    def expect(self, kind: TokenKind) -> Token:
        if self.peekTokenKind() == kind:
            return self.advance()

        else:
            raise SparrowParseError(
                f"Expected {TOKEN_DISPLAY[kind]!r} but got {TOKEN_DISPLAY[self.peekTokenKind()]!r} instead",
                self.peekToken().start,
                self.peekToken().end,
            )

    def parsePrefix(self) -> Expr:
        if self.peekTokenKind() == TokenKind.NUMBER:
            tok = self.advance()
            return NumberLiteral(value=tok.value, start=tok.start, end=tok.end)

        elif self.peekTokenKind() in {TokenKind.TRUE, TokenKind.FALSE}:
            tok = self.advance()
            value = tok.value == "true"
            return BoolLiteral(value=value, start=tok.start, end=tok.end)

        elif self.peekTokenKind() == TokenKind.LPAREN:
            # consume LPAREN
            self.advance()

            # recursively parse full expression inside
            result = self.parseExpr()

            # expect closing RPAREN
            self.expect(TokenKind.RPAREN)

            return result

        elif (
            self.peekTokenKind() == TokenKind.IDENTIFIER
            and self.peekTokenKind(1) == TokenKind.LPAREN
        ):
            funcName = self.advance()
            args, endTok = self.parseArgs()

            return FuncCallExpr(
                name=funcName.value, args=args, start=funcName.start, end=endTok.end
            )

        elif self.peekTokenKind() == TokenKind.IDENTIFIER:
            tok = self.advance()
            return IdentifierExpr(name=tok.value, start=tok.start, end=tok.end)

        elif self.peekTokenKind() in PREFIX_BINDING_POWER:
            opTok = self.advance()
            bp = PREFIX_BINDING_POWER[opTok.kind]
            operand = self.parseExpr(bp)
            return UnaryExpr(
                operator=TOKEN_TO_UNARY_OP[opTok.kind],
                operand=operand,
                start=opTok.start,
                end=operand.end,
            )

        else:
            tok = self.peekToken()

            if tok.kind == TokenKind.EOF:
                raise SparrowParseError(
                    "Unexpected end of input",
                    tok.start,
                    tok.end,
                )

            raise SparrowParseError(
                f"Expected expression, found {tok.value!r}",
                tok.start,
                tok.end,
            )

    def parseExpr(self, min_bp: int = 0) -> Expr:
        left = self.parsePrefix()

        while True:
            kind = self.peekTokenKind()
            if kind not in INFIX_BINDING_POWER:
                break

            bp = INFIX_BINDING_POWER[kind]

            if bp < min_bp:
                break

            op = self.advance()
            right = self.parseExpr(
                bp + 1
            )  # +1 because all four ops are left-associative

            left = BinaryExpr(
                operator=TOKEN_TO_BINARY_OP[op.kind],
                left=left,
                right=right,
                start=left.start,
                end=right.end,
            )

        return left

    def parseArgs(self) -> tuple[tuple[Expr, ...], Token]:
        self.expect(TokenKind.LPAREN)

        args = []

        while self.peekTokenKind() not in {TokenKind.RPAREN, TokenKind.EOF}:
            arg = self.parseExpr()
            args.append(arg)

            if self.peekTokenKind() != TokenKind.RPAREN:
                self.expect(TokenKind.COMMA)

        tok = self.expect(TokenKind.RPAREN)

        return tuple(args), tok

    def parseStatement(self) -> Stmt:
        # assignStmt
        if (
            self.peekTokenKind() == TokenKind.IDENTIFIER
            and self.peekTokenKind(1) == TokenKind.EQ
        ):
            return self.parseAssignStatement()
        # varDeclStmt
        elif (
            self.peekTokenKind() == TokenKind.IDENTIFIER
            and self.peekTokenKind(1) == TokenKind.IDENTIFIER
            and self.peekTokenKind(2) == TokenKind.EQ
        ):
            return self.parseVarDeclStatement()
        # funcDeclStmt
        elif self.peekTokenKind() == TokenKind.FUNCTION:
            return self.parseFuncDeclStatement()
        # returnStmt
        elif self.peekTokenKind() == TokenKind.RETURN:
            return self.parseReturnStatement()
        # ifStmt
        elif self.peekTokenKind() == TokenKind.IF:
            return self.parseIfStatement(isUnless=False)
        elif self.peekTokenKind() == TokenKind.UNLESS:
            return self.parseIfStatement(isUnless=True)
        # whileStmt
        elif self.peekTokenKind() == TokenKind.WHILE:
            return self.parseWhileStatement(isUntil=False)
        elif self.peekTokenKind() == TokenKind.UNTIL:
            return self.parseWhileStatement(isUntil=True)
        elif self.peekTokenKind() == TokenKind.FOREVER:
            return self.parseForeverStatement()
        # repeatStmt
        elif self.peekTokenKind() == TokenKind.REPEAT:
            return self.parseRepeatStatement()
        # stopStmt
        elif self.peekTokenKind() == TokenKind.STOP:
            return self.parseStopStatement()
        # skipStmt
        elif self.peekTokenKind() == TokenKind.SKIP:
            return self.parseSkipStatement()
        # exprStmt
        else:
            value = self.parseExpr()
            self.expect(TokenKind.SEMICOLON)

            return ExprStmt(expr=value, start=value.start, end=value.end)

    def parseAssignStatement(self) -> AssignStmt:
        identifierTok = self.advance()
        self.expect(TokenKind.EQ)

        value = self.parseExpr()
        self.expect(TokenKind.SEMICOLON)

        return AssignStmt(
            name=identifierTok.value,
            value=value,
            start=identifierTok.start,
            end=value.end,
        )

    def parseVarDeclStatement(self) -> VarDeclStmt:
        varType = self.advance()
        varName = self.advance()
        self.expect(TokenKind.EQ)

        varValue = self.parseExpr()
        endTok = self.expect(TokenKind.SEMICOLON)

        return VarDeclStmt(
            type=varType.value,
            name=varName.value,
            value=varValue,
            start=varType.start,
            end=endTok.end,
        )

    def parseFuncDeclStatement(self) -> FuncDeclStmt:
        # consume 'function' keyword
        startTok = self.advance()

        funcName = self.expect(TokenKind.IDENTIFIER)

        params = self.parseParams()

        self.expect(TokenKind.RETURNS)
        returnType = self.expect(TokenKind.IDENTIFIER)

        body, endTok = self.parseBlock()

        return FuncDeclStmt(
            name=funcName.value,
            params=params,
            returnType=returnType.value,
            body=body,
            start=startTok.start,
            end=endTok.end,
        )

    def parseParams(self) -> tuple[Param, ...]:
        self.expect(TokenKind.LPAREN)

        params = []

        while (
            self.peekTokenKind() == TokenKind.IDENTIFIER
            and self.peekTokenKind(1) == TokenKind.IDENTIFIER
        ):
            paramType = self.advance()
            paramName = self.advance()

            param = Param(
                paramType.value, paramName.value, paramType.start, paramName.end
            )
            params.append(param)

            if self.peekTokenKind() != TokenKind.RPAREN:
                self.expect(TokenKind.COMMA)

        self.expect(TokenKind.RPAREN)

        return tuple(params)

    def parseReturnStatement(self) -> ReturnStmt:
        startTok = self.advance()

        retVal = None
        if self.peekTokenKind() != TokenKind.SEMICOLON:
            retVal = self.parseExpr()

        endTok = self.expect(TokenKind.SEMICOLON)

        return ReturnStmt(value=retVal, start=startTok.start, end=endTok.end)

    def parseIfStatement(self, isUnless: bool) -> IfStmt:
        # consume IF token
        ifStartTok = self.advance()
        # parse the condition
        ifCondition = self.parseCondition()
        # parse the block
        ifStmts, ifEndTok = self.parseBlock()

        # check for 'elif' block
        elifClauses = []
        while self.peekTokenKind() == TokenKind.ELIF:
            # consume ELIF token
            elifStartTok = self.advance()
            # parse the condition
            elifCondition = self.parseCondition()
            # parse the block
            elifStmts, elifEndTok = self.parseBlock()

            elifClause = ElifClause(
                condition=elifCondition,
                body=elifStmts,
                start=elifStartTok.start,
                end=elifEndTok.end,
            )
            elifClauses.append(elifClause)

        finalCondition = (
            UnaryExpr(
                UnaryOp.NOT,
                ifCondition,
                start=ifCondition.start,
                end=ifCondition.end,
            )
            if isUnless
            else ifCondition
        )

        elseBody = None
        endTok = elifEndTok if len(elifClauses) > 0 else ifEndTok

        # check for 'else' block
        if self.peekTokenKind() == TokenKind.ELSE:
            # consume ELSE token
            self.advance()
            # parse the block
            elseBody, elseEndTok = self.parseBlock()
            endTok = elseEndTok

        return IfStmt(
            condition=finalCondition,
            ifBody=ifStmts,
            elifClauses=tuple(elifClauses),
            elseBody=elseBody,
            start=ifStartTok.start,
            end=endTok.end,
        )

    def parseWhileStatement(self, isUntil: bool) -> WhileStmt:
        # consume WHILE / UNTIL token
        whileStartTok = self.advance()
        # parse the condition
        whileCondition = self.parseCondition()
        # parse the block
        whileStmts, endTok = self.parseBlock()

        onstopStmts = nostopStmts = None

        if self.peekTokenKind() == TokenKind.ONSTOP:
            self.advance()
            onstopStmts, endTok = self.parseBlock()

        if self.peekTokenKind() == TokenKind.NOSTOP:
            self.advance()
            nostopStmts, endTok = self.parseBlock()

        finalCondition = (
            UnaryExpr(
                UnaryOp.NOT,
                whileCondition,
                start=whileCondition.start,
                end=whileCondition.end,
            )
            if isUntil
            else whileCondition
        )

        return WhileStmt(
            condition=finalCondition,
            body=whileStmts,
            onstop=onstopStmts,
            nostop=nostopStmts,
            start=whileStartTok.start,
            end=endTok.end,
        )

    def parseForeverStatement(self) -> WhileStmt:
        # consume FOREVER token
        foreverStartTok = self.advance()
        # parse the block
        foreverStmts, endTok = self.parseBlock()

        onstopStmts = nostopStmts = None

        if self.peekTokenKind() == TokenKind.ONSTOP:
            self.advance()
            onstopStmts, endTok = self.parseBlock()

        if self.peekTokenKind() == TokenKind.NOSTOP:
            self.advance()
            nostopStmts, endTok = self.parseBlock()

        return WhileStmt(
            condition=BoolLiteral(True, foreverStartTok.start, foreverStartTok.end),
            body=foreverStmts,
            onstop=onstopStmts,
            nostop=nostopStmts,
            start=foreverStartTok.start,
            end=endTok.end,
        )

    def parseRepeatStatement(self) -> RepeatStmt:
        # consume REPEAT token
        repeatStartTok = self.advance()
        # parse the count expression
        repeatCountExpr = self.parseCondition()
        # parse the block
        repeatStmts, endTok = self.parseBlock()

        onstopStmts = nostopStmts = None

        if self.peekTokenKind() == TokenKind.ONSTOP:
            self.advance()
            onstopStmts, endTok = self.parseBlock()

        if self.peekTokenKind() == TokenKind.NOSTOP:
            self.advance()
            nostopStmts, endTok = self.parseBlock()

        return RepeatStmt(
            ntimes=repeatCountExpr,
            body=repeatStmts,
            onstop=onstopStmts,
            nostop=nostopStmts,
            start=repeatStartTok.start,
            end=endTok.end,
        )

    def parseStopStatement(self) -> StopStmt:
        token = self.advance()
        self.expect(TokenKind.SEMICOLON)
        return StopStmt(start=token.start, end=token.end)

    def parseSkipStatement(self) -> SkipStmt:
        token = self.advance()
        self.expect(TokenKind.SEMICOLON)
        return SkipStmt(start=token.start, end=token.end)

    def parseCondition(self) -> Expr:
        self.expect(TokenKind.LPAREN)
        condition = self.parseExpr()
        self.expect(TokenKind.RPAREN)
        return condition

    def parseBlock(self) -> tuple[tuple[Stmt, ...], Token]:
        self.expect(TokenKind.LBRACE)

        stmts = []

        while self.peekTokenKind() not in {
            TokenKind.RBRACE,
            TokenKind.EOF,
        }:
            stmts.append(self.parseStatement())

        endTok = self.expect(TokenKind.RBRACE)

        return tuple(stmts), endTok


def parseProgram(tokens: list[Token]) -> list[Stmt]:
    parser = Parser(tokens)
    statements = []
    while parser.peekTokenKind() != TokenKind.EOF:
        statements.append(parser.parseStatement())
    return statements


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


if __name__ == "__main__":
    from tokenizer import tokenize

    pretty(parseProgram(tokenize("x + 1;")))
