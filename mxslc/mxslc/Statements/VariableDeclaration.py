from . import Statement
from .. import state
from ..Expressions import Expression, StandardLibraryCall
from ..Keyword import DataType
from ..Token import Token


class VariableDeclaration(Statement):
    def __init__(self, data_type: Token, identifier: Token, right: Expression):
        self.data_type = DataType(data_type.type)
        self.identifier = identifier
        self.right = right

    def execute(self) -> None:
        if isinstance(self.right, StandardLibraryCall):
            self.right.assignment_data_type = self.data_type

        node = self.right.evaluate(self.data_type)
        state.add_node(self.identifier, node)
