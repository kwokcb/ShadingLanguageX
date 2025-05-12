import re

from . import Expression
from .. import mtlx
from ..CompileError import CompileError
from ..Keyword import DataType, VECTOR_TYPES, COLOR_TYPES
from ..Token import Token
from ..utils import type_of_swizzle


class SwizzleExpression(Expression):
    def __init__(self, left: Expression, swizzle: Token):
        super().__init__(swizzle, left)
        self.left = left
        self.swizzle = swizzle.lexeme
        self.is_vector_swizzle = re.match(r"[xyzw]", self.swizzle)

    def init(self):
        if not re.fullmatch(r"([xyzw]{1,4}|[rgba]{1,4})", self.swizzle):
            raise CompileError(f"'{self.swizzle}' is not a valid swizzle.", self.token)
        if self.left.data_size < 4 and ("w" in self.swizzle or "a" in self.swizzle):
            raise CompileError(f"'{self.swizzle}' is not a valid swizzle for a {self.left.data_type}.", self.token)
        if self.left.data_size < 3 and ("z" in self.swizzle or "b" in self.swizzle):
            raise CompileError(f"'{self.swizzle}' is not a valid swizzle for a {self.left.data_type}.", self.token)

    @property
    def data_type(self) -> DataType:
        return type_of_swizzle(self.swizzle)

    def create_node(self) -> mtlx.Node:
        valid_types = VECTOR_TYPES if self.is_vector_swizzle else COLOR_TYPES
        left_node = self.left.evaluate(valid_types)

        if len(self.swizzle) == 1:
            return mtlx.extract(left_node, self.swizzle)
        else:
            channels = [mtlx.extract(left_node, c) for c in self.swizzle]
            return mtlx.combine(channels, self.data_type)
