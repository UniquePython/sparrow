from typing import Union

from ast_node import (
    AssignStmt,
    BinaryExpr,
    BinaryOp,
    BooleanLiteral,
    Expr,
    ExprStmt,
    IdentifierExpr,
    IfStmt,
    NumberLiteral,
    Stmt,
    UnaryExpr,
    UnaryOp,
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

PREFIX_BINDING_POWER = {
    TokenKind.MINUS: 7,
}

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
}


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def currToken(self) -> Token:
        return self.tokens[self.pos]

    def currTokenKind(self) -> TokenKind:
        return self.currToken().kind

    def nextToken(self) -> Token:
        return self.tokens[self.pos + 1]

    def nextTokenKind(self) -> TokenKind:
        return self.nextToken().kind

    def advance(self) -> Token:
        tok = self.currToken()
        self.pos += 1
        return tok

    def expect(self, kind: TokenKind) -> Token:
        if self.currTokenKind() == kind:
            return self.advance()

        else:
            raise SparrowParseError(
                f"Expected {TOKEN_DISPLAY[kind]!r} but got {TOKEN_DISPLAY[self.currTokenKind()]!r} instead",
                self.currToken().start,
                self.currToken().end,
            )

    def parsePrefix(self) -> Expr:
        if self.currTokenKind() == TokenKind.NUMBER:
            tok = self.advance()
            return NumberLiteral(value=tok.value, start=tok.start, end=tok.end)

        elif self.currTokenKind() in {TokenKind.TRUE, TokenKind.FALSE}:
            tok = self.advance()
            value = tok.value == "true"
            return BooleanLiteral(value=value, start=tok.start, end=tok.end)

        elif self.currTokenKind() == TokenKind.LPAREN:
            # consume LPAREN
            self.advance()

            # recursively parse full expression inside
            result = self.parseExpr()

            # expect closing RPAREN
            self.expect(TokenKind.RPAREN)

            return result

        elif self.currTokenKind() == TokenKind.IDENTIFIER:
            tok = self.advance()
            return IdentifierExpr(name=tok.value, start=tok.start, end=tok.end)

        elif self.currTokenKind() in PREFIX_BINDING_POWER:
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
            tok = self.currToken()

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
            kind = self.currTokenKind()
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

    def parseStatement(self) -> Stmt:
        # assignStmt
        if (
            self.currTokenKind() == TokenKind.IDENTIFIER
            and self.nextTokenKind() == TokenKind.EQ
        ):
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
        # ifStmt
        elif self.currTokenKind() == TokenKind.IF:
            return self.parseIfStatement()
        # exprStmt
        else:
            value = self.parseExpr()
            self.expect(TokenKind.SEMICOLON)

            return ExprStmt(expr=value, start=value.start, end=value.end)

    def parseIfStatement(self) -> IfStmt:
        # consume IF token
        ifStartTok = self.advance()
        # expect ( for start of condition
        self.expect(TokenKind.LPAREN)
        # parse the condition
        condition = self.parseExpr()
        # expect ) for end of condition and { for start of block
        self.expect(TokenKind.RPAREN)
        self.expect(TokenKind.LBRACE)
        # parse statements until }
        ifStmts = []
        while self.currTokenKind() not in {TokenKind.RBRACE, TokenKind.EOF}:
            ifStmts.append(self.parseStatement())
        # expect closing }
        ifEndTok = self.expect(TokenKind.RBRACE)

        # check for 'else' block
        if self.currTokenKind() == TokenKind.ELSE:
            # consume ELSE token
            self.advance()
            # expect { for start of block
            self.expect(TokenKind.LBRACE)
            # parse statements until }
            elseStmts = []
            while self.currTokenKind() not in {TokenKind.RBRACE, TokenKind.EOF}:
                elseStmts.append(self.parseStatement())
            # expect closing }
            elseEndTok = self.expect(TokenKind.RBRACE)

            return IfStmt(
                condition=condition,
                ifBody=tuple(ifStmts),
                elseBody=tuple(elseStmts),
                start=ifStartTok.start,
                end=elseEndTok.end,
            )

        else:
            return IfStmt(
                condition=condition,
                ifBody=tuple(ifStmts),
                elseBody=None,
                start=ifStartTok.start,
                end=ifEndTok.end,
            )


def parseProgram(tokens: list[Token]) -> list[Stmt]:
    parser = Parser(tokens)
    statements = []
    while parser.currTokenKind() != TokenKind.EOF:
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

        case BooleanLiteral(value=value):
            boolStr = "true" if value else "false"
            print(prefix + connector + boolStr)

        case IdentifierExpr(name=name):
            print(prefix + connector + name)

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

        case IfStmt(condition=condition, ifBody=ifBody, elseBody=elseBody):
            print(prefix + connector + "IF")
            pretty(condition, child_prefix, is_root=False, is_last=len(ifBody) == 0)
            for i, stmt in enumerate(ifBody):
                pretty(stmt, child_prefix, is_root=False, is_last=i == len(ifBody) - 1)
            if elseBody is not None:
                print(prefix + connector + "ELSE")
                for i, stmt in enumerate(elseBody):
                    pretty(
                        stmt,
                        child_prefix,
                        is_root=False,
                        is_last=i == len(elseBody) - 1,
                    )

        case _:
            raise AssertionError(f"unhandled node type: {type(node).__name__}")


if __name__ == "__main__":
    from tokenizer import tokenize

    pretty(parseProgram(tokenize("x + 1;")))
