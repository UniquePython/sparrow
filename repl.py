from environment import Environment
from errors import SparrowError, formatError
from evaluator import execute
from parser import parse, parseProgram, pretty
from tokenizer import tokenize


def run(src: str, env: Environment) -> list[int]:
    tokens = tokenize(src)
    ast = parseProgram(tokens)
    out = []
    for stmt in ast:
        out.append(execute(stmt, env))
    return out


def dumpTokens(src: str) -> None:
    for tok in tokenize(src):
        print(tok)


def dumpAst(src: str) -> None:
    pretty(parse(tokenize(src)))


def main() -> None:
    env = Environment()

    while True:
        try:
            line = input(">>> ")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue

        if not line.strip():
            continue

        src = line

        try:
            if line == ":tokens":
                print("usage: :tokens EXPR")
                continue

            if line.startswith(":tokens "):
                src = line.removeprefix(":tokens ")
                dumpTokens(src)
                continue

            if line == ":ast":
                print("usage: :ast EXPR")
                continue

            if line.startswith(":ast "):
                src = line.removeprefix(":ast ")
                dumpAst(src)
                continue

            if line.startswith(":"):
                command = line.split(maxsplit=1)[0]
                print(f"unknown command {command!r}")
                continue

            outs = run(src, env)
            for out in outs:
                if out is not None:
                    print(out)

        except SparrowError as e:
            print(formatError(e, src))


if __name__ == "__main__":
    main()
