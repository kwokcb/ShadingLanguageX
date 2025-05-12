from . import Expression
from .. import mtlx
from ..Keyword import DataType, Keyword, FILENAME, STRING, FLOAT, INTEGER, BOOLEAN
from ..Token import Token
from ..token_types import INT_LITERAL, FLOAT_LITERAL, FILENAME_LITERAL, STRING_LITERAL


class LiteralExpression(Expression):
    def __init__(self, literal: Token):
        super().__init__(literal)
        self.__literal = literal

    @property
    def data_type(self) -> DataType:
        return {
            Keyword.TRUE: BOOLEAN,
            Keyword.FALSE: BOOLEAN,
            INT_LITERAL: INTEGER,
            FLOAT_LITERAL: FLOAT,
            STRING_LITERAL: STRING,
            FILENAME_LITERAL: FILENAME
        }[self.__literal.type]

    def create_node(self) -> mtlx.Node:
        return mtlx.constant(self.__literal.value)
