from . import Expression
from .. import mtlx
from ..CompileError import CompileError
from ..Keyword import DataType, INTEGER, FLOAT


# TODO implement nested switch expressions (to get 25 cases)
# TODO implement indexed switch expressions
class SwitchExpression(Expression):
    def __init__(self, which: Expression, values: list[Expression]):
        # TODO fix the -1
        super().__init__(-1, which, *values)
        self.which = which
        self.values = values

    def init(self):
        data_type = self.values[0].data_type
        for value in self.values[1:]:
            if value.data_type != data_type:
                raise CompileError(self.line, "All cases must be the same data type.")

    @property
    def data_type(self) -> DataType:
        return self.values[0].data_type

    def create_node(self) -> mtlx.Node:
        node = mtlx.create_node("switch", self.data_type)
        node.set_input("which", self.which.evaluate([INTEGER, FLOAT]))
        for i, value in enumerate(self.values):
            node.set_input(f"in{i+1}", value.evaluate(self.data_type))
        return node
