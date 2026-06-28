from bisect import bisect_right


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
