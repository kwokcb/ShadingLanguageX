from . import Statement
from .. import state
from ..Expressions import Expression, StandardLibraryCall
from ..Keyword import DataType
from ..Token import Token


class VariableDeclaration(Statement):
    def __init__(self, data_type: Token, identifier: Token, right: Expression):
        self.__data_type = DataType(data_type.type)
        self.__identifier = identifier
        self.__right = right

    def execute(self) -> None:
        if isinstance(self.__right, StandardLibraryCall):
            self.__right.assignment_data_type = self.__data_type

        node = self.__right.evaluate(self.__data_type)
        state.add_node(self.__identifier, node)
