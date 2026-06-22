from ast_node import BinaryExpr, NumberLiteral
from errors import SparrowParseError
from tokens import Token, TokenKind

BINDING_POWER = {
    TokenKind.PLUS: 1,
    TokenKind.MINUS: 1,
    TokenKind.ASTERISK: 3,
    TokenKind.FSLASH: 3,
}


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def currToken(self) -> Token:
        return self.tokens[self.pos]

    def currTokenKind(self):
        return self.currToken().kind

    def advance(self) -> Token:
        tok = self.currToken()
        self.pos += 1
        return tok

    def expect(self, kind: TokenKind) -> Token:
        if self.currTokenKind() == kind:
            return self.advance()
        else:
            raise SparrowParseError(
                f"Expected token of kind {kind.name} but found {self.currToken().kind.name}, i.e. {self.currToken().value!r} instead",
                self.currToken().start,
                self.currToken().end,
            )

    def parsePrefix(self):
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
        else:
            raise SparrowParseError(
                f"Illegal prefix {self.currToken().value} found",
                self.currToken().start,
                self.currToken().end,
            )

    def parseExpr(self, min_bp: int = 0):
        left = self.parsePrefix()

        while True:
            kind = self.currTokenKind()
            if kind not in BINDING_POWER:
                break
            bp = BINDING_POWER[kind]
            if bp < min_bp:
                break

            op = self.advance()
            right = self.parseExpr(
                bp + 1
            )  # +1 because all four ops are left-associative
            left = BinaryExpr(
                operator=op.kind,
                left=left,
                right=right,
                start=left.start,
                end=right.end,
            )

        return left


def parse(tokens: list[Token]):
    parser = Parser(tokens)
    ast = parser.parseExpr(0)
    parser.expect(TokenKind.EOF)
    return ast


def pretty(node, prefix="", is_root=True, is_last=True):
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


if __name__ == "__main__":
    from tokenizer import tokenize

    pretty(parse(tokenize("1 + 2 * (3 - 4) / 5")))
