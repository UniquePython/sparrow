from errors import SparrowError, SparrowParseError, formatError
from frontend.lexer.tokenizer import tokenize
from frontend.parser.parser import parseProgram, pretty
from runtime.environment import Environment
from runtime.evaluator import execute
from runtime.values import Value


def run(src: str, prevStmtCount: int, env: Environment) -> tuple[list[Value], int]:
    tokens = tokenize(src)
    ast = parseProgram(tokens)
    newStmts = ast[prevStmtCount:]
    out = []
    for stmt in newStmts:
        res = execute(stmt, env)
        if res is not None:
            out.append(res)
    return out, len(ast)


def dumpTokens(src: str) -> None:
    for tok in tokenize(src):
        print(tok)


def dumpAst(src: str) -> None:
    tokens = tokenize(src)
    ast = parseProgram(tokens)
    for stmt in ast:
        pretty(stmt)


def dumpVar(env: Environment, src: str) -> None:
    if env.exists(src):
        print(env.value(src, 0, 0))
    else:
        print(f"Failed to access undefined variable {src!r}")


def dumpType(env: Environment, src: str) -> None:
    if env.exists(src):
        print(env.type(src, 0, 0))
    else:
        print(f"Failed to access undefined variable {src!r}")


def dumpEnv(env: Environment) -> None:
    for name, (type, value) in env.vars.items():
        print(f"{type} {name} = {value}")


def main() -> None:
    env = Environment()
    fullSrc = ""
    prevStmtCount = 0

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

            if line == ":type":
                print("Usage: :type IDENT")
                continue

            if line.startswith(":type "):
                src = line.removeprefix(":type ")
                dumpType(env, src)
                continue

            if line.startswith(":env"):
                dumpEnv(env)
                continue

            if line.startswith(":newenv"):
                env = Environment()
                continue

            if line.startswith(":"):
                command = line.split(maxsplit=1)[0]
                print(f"Unknown command {command!r}")
                continue

            fullSrc += line + "\n"

            while True:
                try:
                    outs, prevStmtCount = run(fullSrc, prevStmtCount, env)
                    for out in outs:
                        print(out)
                    break
                except SparrowParseError as e:
                    if "end of file" in e.message:
                        try:
                            pendingLine = input("... ")
                        except (EOFError, KeyboardInterrupt):
                            fullSrc = fullSrc[: -len(line) - 1]
                            print()
                            break
                        fullSrc += pendingLine + "\n"
                        line += "\n" + pendingLine
                    else:
                        fullSrc = fullSrc[: -len(line) - 1]
                        print(formatError(e, fullSrc + line))
                        break
                except SparrowError as e:
                    fullSrc = fullSrc[: -len(line) - 1]
                    print(formatError(e, fullSrc + line))
                    break

        except SparrowError as e:
            print(formatError(e, fullSrc))


if __name__ == "__main__":
    main()
