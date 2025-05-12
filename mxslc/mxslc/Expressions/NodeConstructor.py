from . import Expression
from .. import mtlx
from ..Argument import Argument
from ..CompileError import CompileError
from ..Keyword import DataType
from ..Token import Token


# TODO make this work with assignment data type like with standard library calls
# TODO actually, just improve the assignment data type system to work with any expression that wants it
# TODO it doesnt even need to be assignment, let Expression.evaluate handle it instead of VariableDeclaration
class NodeConstructor(Expression):
    def __init__(self, category: Token, data_type: Token, args: list[Argument]):
        super().__init__(category, *[a.expression for a in args])
        self.__category = category.value
        self.__data_type = DataType(data_type.type)
        self.__args = args

    def init(self):
        # Check arguments are valid
        for arg in self.__args:
            if arg.name is None:
                raise CompileError("Unnamed argument in node constructors.", self.token)

    @property
    def data_type(self) -> DataType:
        return self.__data_type

    def create_node(self) -> mtlx.Node:
        node = mtlx.create_node(self.__category, self.data_type)
        for arg in self.__args:
            node.set_input(arg.name, arg.evaluate())
        return node
