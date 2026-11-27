# plox

A tree-walking interpreter for the Lox language, written in Python.

## Status

This is a work in progress.

| Stage | State |
|---|---|
| Scanner (source → tokens) | ✅ Done, including nested `/* */` block comments |
| AST nodes + visitor | ✅ Done for expressions |
| AST printer (debug output) | ✅ Done |
| Expression parser | 🚧 Written, still being debugged |
| Evaluating expressions | ⏳ Not started |
| Statements, variables, scope | ⏳ Not started |
| Control flow, functions, closures | ⏳ Not started |
| Classes and inheritance | ⏳ Not started |

## Running it

You need Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```sh
cd src

# Interactive prompt
uv run python -m plox.lox

# Run a file
uv run python -m plox.lox path/to/script.lox
```

Right now the interpreter parses a single expression and prints its syntax
tree. Evaluation comes next.

> The `plox` console script in `pyproject.toml` still points to a placeholder
> `main()` in `__init__.py`. For now, use `python -m plox.lox`.

### Exit codes

| Code | Meaning |
|---|---|
| `64` | Wrong command-line usage |
| `65` | The script has a syntax error |

## Project layout

```
src/plox/
├── lox.py          # Entry point: REPL, file runner, error reporting
├── scanner.py      # Turns source text into tokens
├── token.py        # Token: type, lexeme, literal value, line
├── token_type.py   # Every kind of token, as an Enum
├── expr.py         # AST node classes and the visitor interface
├── parser.py       # Recursive descent parser: tokens → AST
└── ast_printer.py  # Prints an AST as a Lisp-style string for debugging
```

The data moves through the pipeline like this:

```
source text ──▶ Scanner ──▶ list[Token] ──▶ Parser ──▶ Expr (AST) ──▶ AstPrinter
```

## Design notes

- **AST nodes are frozen dataclasses.** `@dataclass(frozen=True)` gives each
  node a constructor, `__repr__` and equality without any extra code, and the
  nodes can't be changed after they're created.
- **The visitor is a generic ABC.** `ExprVisitor[R]` uses `Generic[R]` and
  `@abstractmethod`. If a visitor forgets a method, Python raises an error
  when you create it, not halfway through a run.
- **`error()` dispatches on its argument's type.** `Lox.error` uses
  `functools.singledispatchmethod`, so it accepts either a line number (from
  the scanner) or a `Token` (from the parser).
- **The parser's `match()` takes `*types`,** so one call can check for any of
  several token types.
- **`ParseError` is a plain `Exception` subclass.** The parser raises it to
  unwind back to `parse()`.
- **The interpreter's state lives on an object.** `had_error` is an attribute
  on a `Lox` instance, and the scanner and parser get that instance passed in.
  There's no global state.
- **Error recovery uses `match`/`case`.** The parser uses structural pattern
  matching to find the start of the next statement after a syntax error.

## Extras

- **Nested block comments.** `/* outer /* inner */ still a comment */` works,
  because the scanner tracks how deep it is instead of stopping at the first
  `*/`.

## Development

The code is formatted with [ruff](https://docs.astral.sh/ruff/):

```sh
uvx ruff format src
```
