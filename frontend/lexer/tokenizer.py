from string import ascii_lowercase, ascii_uppercase, digits

from errors import SparrowLexError
from frontend.lexer.tokens import (
    KEYWORDS_TO_TOKENKIND,
    MULTI_CHAR_TOKENS,
    SINGLE_CHAR_TOKENS,
    Token,
    TokenKind,
)

IDENTIFIER_STARTING_CHARS = "_" + ascii_lowercase + ascii_uppercase
IDENTIFIER_CHARS = IDENTIFIER_STARTING_CHARS + digits

IDENTIFIER_STARTING_CHARS_FS = frozenset(IDENTIFIER_STARTING_CHARS)
IDENTIFIER_CHARS_FS = frozenset(IDENTIFIER_CHARS)


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

        # handle identifiers
        elif char in IDENTIFIER_STARTING_CHARS_FS:
            start = cursor
            while cursor < srcLen and src[cursor] in IDENTIFIER_CHARS_FS:
                cursor += 1

            identifier = src[start:cursor]

            if identifier in KEYWORDS_TO_TOKENKIND:
                tokens.append(
                    Token(KEYWORDS_TO_TOKENKIND[identifier], identifier, start, cursor)
                )
            else:
                tokens.append(Token(TokenKind.IDENTIFIER, identifier, start, cursor))

        # handle multi-char tokens
        elif char in MULTI_CHAR_TOKENS:
            unit = src[cursor : cursor + 2] if cursor + 1 < srcLen else char
            if unit in MULTI_CHAR_TOKENS:
                tokens.append(Token(MULTI_CHAR_TOKENS[unit], unit, cursor, cursor + 2))
                cursor += 2
            else:
                tokens.append(Token(MULTI_CHAR_TOKENS[char], char, cursor, cursor + 1))
                cursor += 1

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
    toks = tokenize("== != <= >= = ! < >")
    for tok in toks:
        print(tok)
