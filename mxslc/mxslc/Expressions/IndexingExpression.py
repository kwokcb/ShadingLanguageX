from mxslc import mtlx
from mxslc.Expressions import Expression
from mxslc.Keyword import DataType, FLOAT, INTEGER, VECTOR_TYPES, COLOR_TYPES


class IndexingExpression(Expression):
    def __init__(self, expr: Expression, indexer: Expression):
        super().__init__(indexer.line, expr, indexer)
        self.__expr = expr
        self.__indexer = indexer

    @property
    def data_type(self) -> DataType:
        return FLOAT

    def create_node(self) -> mtlx.Node:
        index = self.__indexer.evaluate(INTEGER)
        value = self.__expr.evaluate(VECTOR_TYPES + COLOR_TYPES)
        return mtlx.extract(value, index)
