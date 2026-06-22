from errors import SparrowError, formatError
from evaluator import evaluate
from parser import parse
from tokenizer import tokenize


def main():
    while True:
        try:
            line = input(">>> ")
        except EOFError:
            break
        if not line.strip():
            continue
        try:
            tokens = tokenize(line)
            ast = parse(tokens)
            result = evaluate(ast)
            print(result)
        except SparrowError as e:
            print(formatError(e, line))


if __name__ == "__main__":
    main()
