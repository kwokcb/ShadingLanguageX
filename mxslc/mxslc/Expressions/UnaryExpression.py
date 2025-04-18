from . import Expression
from .. import mtlx
from ..Keyword import DataType, Keyword, BOOLEAN, NUMERIC_TYPES
from ..Token import Token


class UnaryExpression(Expression):
    def __init__(self, operator: Token, right: Expression):
        super().__init__(operator.line, right)
        self.operator = operator
        self.right = right

    @property
    def data_type(self) -> DataType:
        return self.right.data_type

    def create_node(self) -> mtlx.Node:
        if self.operator in ["!", Keyword.NOT]:
            node = mtlx.create_node("not", BOOLEAN)
            node.set_input("in", self.right.evaluate(BOOLEAN))
            return node
        elif self.operator == "-":
            right_node = self.right.evaluate(NUMERIC_TYPES)
            node = mtlx.create_node("subtract", right_node.data_type)
            node.set_input("in1", right_node.data_type.zeros())
            node.set_input("in2", right_node)
            return node
        else:
            return self.right.evaluate(NUMERIC_TYPES)
