from ast_node import NumberLiteral
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
            raise TypeError(
                f"Expected token of kind {kind} but found {self.currToken().kind}, i.e. {self.currToken()} instead"
            )

    def parsePrefix(self):
        if self.currTokenKind() == TokenKind.NUMBER:
            tok = self.advance()
            return NumberLiteral(tok.value)
        elif self.currTokenKind() == TokenKind.LPAREN:
            # consume LPAREN
            self.advance()

            # recursively parse full expression inside
            result = self.parseExpr()

            # expect closing RPAREN
            self.expect(TokenKind.RPAREN)

            return result
        else:
            raise ValueError(f"Illegal prefix {self.currToken()} found")
