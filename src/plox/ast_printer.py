from .expr import Binary, Unary, Literal, Grouping, Expr, ExprVisitor


class AstPrinter(ExprVisitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expression(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary_expression(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def visit_grouping_expression(self, expr: Grouping) -> str:
        return self._parenthesize("group", expr.expression)

    def visit_literal_expression(self, expr: Literal) -> str:
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        parts = " ".join(e.accept(self) for e in exprs)
        return f"{name} {parts}"


if __name__ == "__main__":
    from .token import Token
    from .token_type import TokenType

    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )

    print(AstPrinter().print(expression))
