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
    line, col = offsetToLineCol(lineStarts, err.start)

    code = src.splitlines()[line - 1]

    nCarets = max(1, err.end - err.start)
    gutterWidth = len(str(line))

    blankGutter = f"{'':>{gutterWidth}} | "
    codeGutter = f"{line:>{gutterWidth}} | {code}"
    caretGutter = blankGutter + " " * (col - 1)

    errMsg = ""

    errMsg += f"error: {err.message}\n"
    errMsg += f"---> line {line}, col {col}\n"

    errMsg += blankGutter + "\n"
    errMsg += codeGutter + "\n"
    errMsg += caretGutter + "^" * nCarets

    return errMsg


if __name__ == "__main__":
    src = "1 +\n2 *\n(3)"
    print(offsetToLineCol(src, 2))
    print(offsetToLineCol(src, 9))
