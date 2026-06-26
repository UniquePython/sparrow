class StopSignal(Exception):
    pass


class SkipSignal(Exception):
    pass


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


class SparrowRuntimeError(SparrowError):
    pass


def offsetToLineCol(src: str, offset: int) -> tuple[int, int]:
    newLines = 1
    distSinceLastNewline = 1
    for i in range(offset):
        char = src[i]
        if char == "\n":
            newLines += 1
            distSinceLastNewline = 1
        else:
            distSinceLastNewline += 1
    return (newLines, distSinceLastNewline)


def formatError(err: SparrowError, src: str) -> str:
    line, col = offsetToLineCol(src, err.start)

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
