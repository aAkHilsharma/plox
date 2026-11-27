import sys
from pathlib import Path
from functools import singledispatchmethod

from .token import Token
from .token_type import TokenType
from .scanner import Scanner
from .parser import Parser
from .ast_printer import AstPrinter


class Lox:
    def __init__(self) -> None:
        self.had_error = False

    def run_file(self, path: str) -> None:
        source: str = Path(path).read_text(encoding="utf-8")
        self.run(source)
        if self.had_error:
            sys.exit(65)

    def run_prompt(self) -> None:
        while True:
            try:
                line: str = input("> ")
            except EOFError:
                print()
                break
            self.run(line)
            self.had_error = False

    def run(self, source: str) -> None:
        scanner = Scanner(source, self)
        tokens = scanner.scanTokens()

        parser = Parser(tokens, self)
        expr = parser.parse()

        # Stop if there was a syntax error
        if self.had_error:
            return

        print(AstPrinter().print(expr))

    @singledispatchmethod
    def error(self, where: object, message: str) -> None:
        raise TypeError(f"Unsupported type: {type(where)}")

    @error.register
    def _(self, line: int, message: str):
        self.report(line, "", message)

    @error.register
    def _(self, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)

    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        self.had_error = True

    def main(self, args: list[str]) -> None:
        if len(args) > 1:
            print("Usage plox [script]")
            sys.exit(64)
        elif len(args) == 1:
            self.run_file(args[0])
        else:
            self.run_prompt()


if __name__ == "__main__":
    Lox().main(sys.argv[1:])
