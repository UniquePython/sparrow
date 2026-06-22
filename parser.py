from tokens import Token, TokenKind


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def currToken(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.currToken()
        self.pos += 1
        return tok

    def expect(self, kind: TokenKind) -> Token:
        if self.currToken().kind == kind:
            return self.advance()
        else:
            raise TypeError(
                f"Expected token of kind {kind} but found {self.currToken().kind}, i.e. {self.currToken()} instead"
            )
