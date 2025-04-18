from . import Expression
from .. import mtlx
from ..Keyword import DataType


class GroupingExpression(Expression):
    def __init__(self, expr: Expression):
        # TODO fix the -1
        super().__init__(-1, expr)
        self.expr = expr

    @property
    def data_type(self) -> DataType:
        return self.expr.data_type

    def create_node(self) -> mtlx.Node:
        return self.expr.evaluate()
