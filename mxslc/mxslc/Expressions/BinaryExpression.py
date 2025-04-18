from abc import ABC

from . import Expression
from .. import mtlx
from ..CompileError import CompileError
from ..Keyword import DataType, INTEGER, FLOAT_TYPES, NUMERIC_TYPES, BOOLEAN, FLOAT, Keyword
from ..Token import Token
from ..utils import one


class BinaryExpression(Expression, ABC):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        super().__init__(operator.line, left, right)
        self.left = left
        self.operator = operator
        self.right = right


class ArithmeticExpression(BinaryExpression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        super().__init__(left, operator, right)
        self.node_type = {
            "+": "add",
            "-": "subtract",
            "*": "multiply",
            "/": "divide",
            "%": "modulo",
            "^": "power"
        }[self.operator.type]

    def init(self):
        if one(e.data_type == INTEGER for e in [self.left, self.right]):
            raise CompileError(self.line, "Integers cannot be combined with other types.")
        if all(e.data_size > 1 for e in [self.left, self.right]) and self.left.data_type != self.right.data_type:
            raise CompileError(self.line, f"Cannot {self.node_type} a {self.left.data_type} and a {self.right.data_type}.")

    @property
    def data_type(self) -> DataType:
        if self.left.data_size > self.right.data_size:
            return self.left.data_type
        else:
            return self.right.data_type

    def create_node(self) -> mtlx.Node:
        valid_types = FLOAT_TYPES
        if self.node_type in ["add", "subtract"]:
            valid_types = NUMERIC_TYPES

        left_node = self.left.evaluate(valid_types)
        right_node = self.right.evaluate(valid_types)

        if left_node.data_size < right_node.data_size:
            left_node = mtlx.convert(left_node, right_node.data_type)

        node = mtlx.create_node(self.node_type, self.data_type)
        node.set_input("in1", left_node)
        node.set_input("in2", right_node)
        return node


class ComparisonExpression(BinaryExpression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        super().__init__(left, operator, right)

    def init(self):
        if self.left.data_type != self.right.data_type:
            raise CompileError(self.line, f"Cannot compare a {self.left.data_type} and a {self.right.data_type}.")

    @property
    def data_type(self) -> DataType:
        return BOOLEAN

    def create_node(self) -> mtlx.Node:
        node_type = {
            "!=": "ifequal",
            "==": "ifequal",
            ">": "ifgreater",
            "<": "ifgreatereq",
            ">=": "ifgreatereq",
            "<=": "ifgreater"
        }[self.operator.type]

        valid_types = [BOOLEAN, INTEGER, FLOAT]
        left_node = self.left.evaluate(valid_types)
        right_node = self.right.evaluate(valid_types)

        if self.operator in ["<", "<="]:
            left_node, right_node = right_node, left_node

        comp_node = mtlx.create_node(node_type, BOOLEAN)
        comp_node.set_input("value1", left_node)
        comp_node.set_input("value2", right_node)

        if node_type == "!=":
            bang_node = mtlx.create_node("not", BOOLEAN)
            bang_node.set_input("in", comp_node)
            return bang_node
        else:
            return comp_node


class LogicExpression(BinaryExpression):
    def __init__(self, left: Expression, operator: Token, right: Expression):
        super().__init__(left, operator, right)

    @property
    def data_type(self) -> DataType:
        return BOOLEAN

    def create_node(self) -> mtlx.Node:
        node_type = {
            "&": "and",
            Keyword.AND: "and",
            "|": "or",
            Keyword.OR: "or"
        }[self.operator.type]

        node = mtlx.create_node(node_type, BOOLEAN)
        node.set_input("in1", self.left.evaluate(BOOLEAN))
        node.set_input("in2", self.right.evaluate(BOOLEAN))
        return node
