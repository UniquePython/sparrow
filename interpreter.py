import sys

from errors import SparrowError, computeLineStarts, formatError
from frontend.lexer.tokenizer import tokenize
from frontend.parser.parser import parseProgram
from runtime.environment import Environment
from runtime.evaluator import execute
from semantic.type_environment import TypeEnvironment
from semantic.typecheck import checkStmt


def main() -> None:
    # 1. read path from argv, read file
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input-file>")
        exit(1)

    path = sys.argv[1]
    with open(path, "r") as file:
        src = file.read()

    lineStarts = computeLineStarts(src)

    # 2. tokenize + parse (catch SparrowError -> formatError -> print -> exit)
    try:
        tokens = tokenize(src)
    except SparrowError as e:
        print(formatError(e, src, lineStarts))
        exit(2)

    try:
        ast = parseProgram(tokens)
    except SparrowError as e:
        print(formatError(e, src, lineStarts))
        exit(3)

    # 3. typecheck every statement against one fresh TypeEnvironment (catch + report + exit on failure)
    typeEnv = TypeEnvironment()
    for stmt in ast:
        try:
            checkStmt(
                stmt,
                typeEnv,
                False,
            )
        except SparrowError as e:
            print(formatError(e, src, lineStarts))
            exit(4)

    # 4. only if all passed: execute every statement against one fresh Environment, print non-None results
    env = Environment()
    for stmt in ast:
        try:
            out = execute(stmt, env)
            if out is not None:
                print(out)
        except SparrowError as e:
            print(formatError(e, src, lineStarts))
            exit(5)


if __name__ == "__main__":
    main()
