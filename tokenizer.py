from errors import SparrowLexError
from tokens import SINGLE_CHAR_TOKENS, Token, TokenKind


def tokenize(src: str) -> list[Token]:
    tokens = []
    cursor = 0
    srcLen = len(src)

    while cursor < srcLen:
        char = src[cursor]

        # skip whitespace
        if char.isspace():
            cursor += 1
            continue

        # skip comments
        if char == "#":
            while cursor < srcLen and src[cursor] != "\n":
                cursor += 1
            continue

        # handle multi-digit numbers
        elif "0" <= char <= "9":
            start = cursor
            while cursor < srcLen and "0" <= src[cursor] <= "9":
                cursor += 1

            tokens.append(
                Token(TokenKind.NUMBER, int(src[start:cursor]), start, cursor)
            )

        # handle single-char tokens
        elif char in SINGLE_CHAR_TOKENS:
            kind = SINGLE_CHAR_TOKENS[char]
            tokens.append(Token(kind, char, cursor, cursor + 1))
            cursor += 1

        # handle unrecognized characters
        else:
            raise SparrowLexError(f"Unexpected character {char!r}", cursor, cursor + 1)

    tokens.append(Token(TokenKind.EOF, None, cursor, cursor))
    return tokens


if __name__ == "__main__":
    toks = tokenize("  1 +   (2  -  4)  * 8   / 16 # comment")
    for tok in toks:
        print(tok)
