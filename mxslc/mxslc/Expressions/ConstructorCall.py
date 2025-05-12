from . import Expression
from .. import mtlx
from ..Argument import Argument
from ..Keyword import DataType, FLOAT_TYPES
from ..Token import Token


class ConstructorCall(Expression):
    def __init__(self, data_type: Token, args: list[Argument]):
        super().__init__(data_type, *[a.expression for a in args])
        self.__data_type = DataType(data_type.type)
        self.__args = args

    @property
    def data_type(self) -> DataType:
        return self.__data_type

    def create_node(self) -> mtlx.Node:
        if len(self.__args) == 0:
            return self._create_constant_node()
        elif len(self.__args) == 1:
            return self._create_convert_node()
        else:
            return self._create_combine_node()

    def _create_constant_node(self) -> mtlx.Node:
        return mtlx.constant(self.data_type.zeros())

    def _create_convert_node(self) -> mtlx.Node:
        return mtlx.convert(self.__args[0].evaluate(), self.data_type)

    def _create_combine_node(self) -> mtlx.Node:
        channels = []
        # fill channels with args
        for arg in self.__args:
            new_channels = mtlx.extract_all(arg.evaluate(FLOAT_TYPES))
            for new_channel in new_channels:
                channels.append(new_channel)
                if len(channels) == self.data_size:
                    return mtlx.combine(channels, self.data_type)
        # fill remaining channels (if any) with zeros
        while len(channels) < self.data_size:
            channels.append(mtlx.constant(0.0))
        return mtlx.combine(channels, self.data_type)
