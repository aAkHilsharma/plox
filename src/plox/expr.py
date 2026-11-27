from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from .token import Token

R = TypeVar("R")


class ExprVisitor(ABC, Generic[R]):
    @abstractmethod
    def visit_binary_expression(self, expr: Binary) -> R: ...

    @abstractmethod
    def visit_unary_expression(self, expr: Unary) -> R: ...

    @abstractmethod
    def visit_grouping_expression(self, expr: Grouping) -> R: ...

    @abstractmethod
    def visit_literal_expression(self, expr: Literal) -> R: ...


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor[R]) -> R: ...


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_binary_expression(self)


@dataclass(frozen=True)
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_grouping_expression(self)


@dataclass(frozen=True)
class Literal(Expr):
    value: Any

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_literal_expression(self)


@dataclass(frozen=True)
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor[R]) -> R:
        return visitor.visit_unary_expression(self)
