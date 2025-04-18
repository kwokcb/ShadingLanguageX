from . import Expression
from .. import state, mtlx
from ..Keyword import DataType
from ..Token import Token


class IdentifierExpression(Expression):
    def __init__(self, identifier: Token):
        super().__init__(identifier.line)
        self.__identifier = identifier

    @property
    def data_type(self) -> DataType:
        node = state.get_node(self.__identifier)
        return node.data_type

    def create_node(self) -> mtlx.Node:
        old_node = state.get_node(self.__identifier)
        new_node = mtlx.create_node("dot", self.data_type)
        new_node.set_input("in", old_node)
        return new_node
