from . import Expression
from .. import mtlx
from ..Argument import Argument
from ..CompileError import CompileError
from ..Keyword import DataType, FLOAT_TYPES
from ..StandardLibrary import StandardLibrary
from ..Token import Token


# TODO named arguments are not working
class StandardLibraryCall(Expression):
    def __init__(self, func: Token, args: list[Argument]):
        super().__init__(func, *[a.expression for a in args])
        self.func = StandardLibrary(func.lexeme)
        self.args = args
        # TODO extend this to work in other places, if multiple types are allowed, fill the largest color, then largest vector
        # this will be set externally before evaluate is called
        self.assignment_data_type = None

    def init(self):
        # check named arguments always come after positional arguments
        args_are_named = False
        for arg in self.args:
            if arg.is_named:
                args_are_named = True
            elif args_are_named:
                raise CompileError(f"Named arguments must come after positional argument.", self.token)

        # check number of arguments
        if len(self.args) > len(self.func.parameters(self.args)):
            raise CompileError(f"Too many arguments given for function '{self.func}'.", self.token)

        # check named arguments have valid names
        for arg in self.args:
            if arg.is_named and arg.name not in [a.name for a in self.func.parameters(self.args)]:
                raise CompileError(f"Invalid named argument for function '{self.func}'.", self.token)

    @property
    def data_type(self) -> DataType:
        arg0_data_type = self.args[0].data_type if len(self.args) > 0 else None
        return self.func.return_type(self.assignment_data_type, arg0_data_type)

    def create_node(self) -> mtlx.Node:
        # special case for min and max which allow any number of parameters
        if self.func in [StandardLibrary.MIN, StandardLibrary.MAX]:
            return self.create_min_max_nodes()

        # default function behaviour
        node = mtlx.create_node(self.func, self.data_type)
        func_params = self.func.parameters(self.args)

        for i, arg in enumerate(self.args):
            if arg.is_positional:
                param = func_params[i]
            else:
                param = func_params[arg.name]
            node.set_input(param.name, arg.evaluate(param.data_types))
        return node

    def create_min_max_nodes(self) -> mtlx.Node:
        if len(self.args) < 2:
            raise CompileError(f"Not enough arguments for function '{self.func}'.", self.token)
        if any(arg.data_type != self.args[0].data_type for arg in self.args):
            raise CompileError(f"All arguments must have the same data type for function '{self.func}'.", self.token)

        # iteratively create min nodes or max nodes until all parameters have been included
        node = mtlx.create_node(self.func, self.data_type)
        node.set_input("in1", self.args[0].evaluate(FLOAT_TYPES))
        node.set_input("in2", self.args[1].evaluate(FLOAT_TYPES))
        for arg in self.args[2:]:
            n = mtlx.create_node(self.func, self.data_type)
            n.set_input("in1", arg.evaluate(FLOAT_TYPES))
            n.set_input("in2", node)
            node = n
        return node
