from __future__ import annotations

from abc import ABC, abstractmethod

from .. import mtlx
from ..CompileError import CompileError
from ..Keyword import DataType, INTEGER, FLOAT, DATA_TYPES
from ..Token import Token
from ..utils import as_list


class Expression(ABC):
    def __init__(self, token: Token, *child_expressions: Expression):
        self.__token = token
        self.__child_expressions = child_expressions
        self.__initialized = False

    def __init(self):
        for child_expression in self.__child_expressions:
            if child_expression:
                child_expression.__init()
        if not self.__initialized:
            self.init()
            self.__initialized = True

    #virtualmethod
    def init(self):
        ...

    @property
    @abstractmethod
    def data_type(self) -> DataType:
        ...

    @property
    def data_size(self) -> int:
        return self.data_type.size

    @property
    def token(self) -> Token:
        return self.__token

    def evaluate(self, valid_types: DataType | list[DataType] = None) -> mtlx.Node:
        self.__init()
        node = self.create_node()
        assert node.data_type == self.data_type

        valid_types = as_list(valid_types) or DATA_TYPES
        node = _implicit_int_to_float(node, valid_types)
        if node.data_type not in valid_types:
            raise CompileError(f"Invalid data type. Expected one of {valid_types}, but got {node.data_type}.", self.token)

        return node

    @abstractmethod
    def create_node(self) -> mtlx.Node:
        ...


def _implicit_int_to_float(node: mtlx.Node, valid_types: list[DataType]) -> mtlx.Node:
    is_int = node.data_type is INTEGER
    int_is_valid = INTEGER in valid_types
    float_is_valid = FLOAT in valid_types
    if is_int and not int_is_valid and float_is_valid:
        return mtlx.convert(node, FLOAT)
    else:
        return node
