from . import Expression
from .. import state, mtlx
from ..Argument import Argument
from ..Keyword import DataType
from ..Token import Token


class FunctionCall(Expression):
    """
    Represents a call to a user-defined function.
    """
    def __init__(self, identifier: Token, args: list[Argument]):
        super().__init__(identifier.line, *[a.expression for a in args])
        self.__func = None
        self.__identifier = identifier
        self.__args = args

    def init(self):
        self.__func = state.get_function(self.__identifier)

    @property
    def data_type(self) -> DataType:
        return self.__func.data_type

    def create_node(self) -> mtlx.Node:
        return self.__func.invoke(self.__args)
