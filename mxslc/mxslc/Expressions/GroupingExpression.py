from . import Expression
from .. import mtlx
from ..Keyword import DataType


class GroupingExpression(Expression):
    def __init__(self, expr: Expression):
        super().__init__(expr.line, expr)
        self.__expr = expr

    @property
    def data_type(self) -> DataType:
        return self.__expr.data_type

    def create_node(self) -> mtlx.Node:
        return self.__expr.evaluate()
