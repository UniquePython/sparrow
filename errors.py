from bisect import bisect_right
from typing import Optional


class SparrowError(Exception):
    def __init__(self, message: str, start: int, end: int):
        self.message = message
        self.start = start
        self.end = end
        super().__init__(message)


class SparrowLexError(SparrowError):
    pass


class SparrowParseError(SparrowError):
    pass


class SparrowTypeError(SparrowError):
    pass


class SparrowRuntimeError(SparrowError):
    pass


def computeLineStarts(src: str) -> list[int]:
    lineStarts = [0]
    pos = src.find("\n")
    while pos != -1:
        lineStarts.append(pos + 1)
        pos = src.find("\n", pos + 1)
    return lineStarts


def offsetToLineCol(lineStarts: list[int], offset: int) -> tuple[int, int]:
    lineIdx = bisect_right(lineStarts, offset) - 1
    line = lineIdx + 1
    column = offset - lineStarts[lineIdx] + 1
    return (line, column)


def levenshtein(a: str, b: str) -> int:
    m = len(a)
    n = len(b)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # deletion
                    dp[i][j - 1],  # insertion
                    dp[i - 1][j - 1],  # substitution
                )

    return dp[m][n]


def suggestClosest(typo: str, candidates: list[str]) -> Optional[str]:
    threshold = max(1, len(typo) // 2)

    qualifying: list[tuple[str, int]] = []

    typo = typo.lower()

    for candidate in candidates:
        dist = levenshtein(typo, candidate.lower())
        if dist <= threshold:
            qualifying.append((candidate, dist))

    if not qualifying:
        return None

    best = min(dist for _, dist in qualifying)
    remaining = [candidate for candidate, dist in qualifying if dist == best]

    if len(remaining) == 1:
        return f"Maybe you meant {remaining[0]!r}?"

    return f"Maybe you meant one of " f"{', '.join(repr(c) for c in remaining)}?"


def formatError(err: SparrowError, src: str, lineStarts: list[int]) -> str:
    startLine, startCol = offsetToLineCol(lineStarts, err.start)
    endLine, endCol = offsetToLineCol(lineStarts, err.end)

    lines = src.splitlines()
    gutterWidth = len(str(endLine))
    blankGutter = f"{'':>{gutterWidth}} | "

    errMsg = ""
    errMsg += f"error: {err.message}\n"
    errMsg += f"---> line {startLine}, col {startCol}\n"
    errMsg += blankGutter + "\n"

    rows = []
    for lineNum in range(startLine, endLine + 1):
        code = lines[lineNum - 1]

        caretStartCol = 1
        caretEndCol = len(code) + 1

        if lineNum == startLine:
            caretStartCol = startCol
        if lineNum == endLine:
            caretEndCol = endCol

        nCarets = max(1, caretEndCol - caretStartCol)

        codeGutter = f"{lineNum:>{gutterWidth}} | {code}"
        caretGutter = blankGutter + " " * (caretStartCol - 1)

        rows.append(codeGutter)
        rows.append(caretGutter + "^" * nCarets)

    errMsg += "\n".join(rows)

    return errMsg


if __name__ == "__main__":
    src = "1 +\n2 *\n(3)"
    print(offsetToLineCol(src, 2))
    print(offsetToLineCol(src, 9))
