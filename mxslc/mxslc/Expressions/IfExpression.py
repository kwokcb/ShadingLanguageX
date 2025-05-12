from . import Expression
from .. import mtlx
from ..CompileError import CompileError
from ..Keyword import DataType, BOOLEAN, NUMERIC_TYPES
from ..Token import Token


# TODO implement if else
class IfExpression(Expression):
    def __init__(self, token: Token, clause: Expression, then: Expression, otherwise: Expression):
        # TODO fix the -1
        super().__init__(token, clause, then, otherwise)
        self.clause = clause
        self.then = then
        self.otherwise = otherwise

    def init(self):
        if self.then.data_type != self.otherwise.data_type:
            raise CompileError(f"Branches must be of same data type, but were {self.then.data_type} and {self.otherwise.data_type}.", self.token)

    @property
    def data_type(self) -> DataType:
        return self.then.data_type

    def create_node(self) -> mtlx.Node:
        clause_node = self.clause.evaluate(BOOLEAN)
        then_node = self.then.evaluate(NUMERIC_TYPES)
        otherwise_node = self.otherwise.evaluate(NUMERIC_TYPES)

        node = mtlx.create_node("ifequal", self.data_type)
        node.set_input("value1", clause_node)
        node.set_input("value2", True)
        node.set_input("in1", then_node)
        node.set_input("in2", otherwise_node)

        return node
