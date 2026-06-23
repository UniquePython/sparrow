from ast_node import (
    AssignStmt,
    BinaryExpr,
    BinaryOp,
    Expr,
    ExprStmt,
    IdentifierExpr,
    NumberLiteral,
    Stmt,
    UnaryExpr,
    UnaryOp,
)
from errors import SparrowParseError
from tokens import TOKEN_DISPLAY, Token, TokenKind

INFIX_BINDING_POWER = {
    TokenKind.PLUS: 1,
    TokenKind.MINUS: 1,
    TokenKind.ASTERISK: 3,
    TokenKind.FSLASH: 3,
    TokenKind.PERCENT: 3,
}

PREFIX_BINDING_POWER = {
    TokenKind.MINUS: 5,
}

TOKEN_TO_BINARY_OP = {
    TokenKind.PLUS: BinaryOp.ADD,
    TokenKind.MINUS: BinaryOp.SUB,
    TokenKind.ASTERISK: BinaryOp.MUL,
    TokenKind.FSLASH: BinaryOp.DIV,
    TokenKind.PERCENT: BinaryOp.MOD,
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
        if (
            self.currTokenKind() == TokenKind.IDENTIFIER
            and self.nextTokenKind() == TokenKind.EQ
        ):
            # assignStmt
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
        else:
            # exprStmt
            value = self.parseExpr()
            self.expect(TokenKind.SEMICOLON)

            return ExprStmt(expr=value, start=value.start, end=value.end)


def parse(tokens: list[Token]) -> Expr:
    parser = Parser(tokens)
    ast = parser.parseExpr(0)
    parser.expect(TokenKind.EOF)
    return ast


def parseProgram(tokens: list[Token]) -> list[Stmt]:
    parser = Parser(tokens)
    statements = []
    while parser.currTokenKind() != TokenKind.EOF:
        statements.append(parser.parseStatement())
    return statements


def pretty(node: Expr, prefix="", is_root=True, is_last=True) -> None:
    if is_root:
        connector = ""
    elif not is_root and is_last:
        connector = "└── "
    else:
        connector = "├── "

    if isinstance(node, NumberLiteral):
        print(prefix + connector + str(node.value))

    elif isinstance(node, BinaryExpr):
        print(prefix + connector + node.operator.name)
        child_prefix = prefix + ("" if is_root else ("    " if is_last else "│   "))
        pretty(node.left, child_prefix, is_root=False, is_last=False)
        pretty(node.right, child_prefix, is_root=False, is_last=True)

    elif isinstance(node, UnaryExpr):
        print(prefix + connector + node.operator.name)
        child_prefix = prefix + ("" if is_root else ("    " if is_last else "│   "))
        pretty(node.operand, child_prefix, is_root=False, is_last=True)

    elif isinstance(node, IdentifierExpr):
        print(prefix + connector + node.name)


if __name__ == "__main__":
    from tokenizer import tokenize

    pretty(parse(tokenize("x + 1")))
