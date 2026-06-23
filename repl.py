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


def dumpVar(env: Environment, src: str) -> None:
    if src in env.vars:
        print(env.get(src, 0, 0))
    else:
        print(f"Failed to access undefined variable {src!r}")


def dumpEnv(env: Environment) -> None:
    for var, value in env.vars.items():
        print(f"{var} = {value}")


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
                print("Usage: :tokens EXPR")
                continue

            if line.startswith(":tokens "):
                src = line.removeprefix(":tokens ")
                dumpTokens(src)
                continue

            if line == ":ast":
                print("Usage: :ast EXPR")
                continue

            if line.startswith(":ast "):
                src = line.removeprefix(":ast ")
                dumpAst(src)
                continue

            if line == ":var":
                print("Usage: :var IDENT")
                continue

            if line.startswith(":var "):
                src = line.removeprefix(":var ")
                dumpVar(env, src)
                continue

            if line.startswith(":env"):
                src = line.removeprefix(":env")
                dumpEnv(env)
                continue

            if line.startswith(":"):
                command = line.split(maxsplit=1)[0]
                print(f"Unknown command {command!r}")
                continue

            outs = run(src, env)
            for out in outs:
                if out is not None:
                    print(out)

        except SparrowError as e:
            print(formatError(e, src))


if __name__ == "__main__":
    main()
