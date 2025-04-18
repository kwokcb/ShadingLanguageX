from . import VariableAssignment
from ..Expressions import Expression, IdentifierExpression, SwizzleExpression, ArithmeticExpression, LogicExpression
from ..Token import Token


class CompoundAssignment(VariableAssignment):
    def __init__(self, identifier: Token, swizzle: Token, operator: Token, right: Expression):
        binary_op = Token(operator.lexeme[0])

        left = IdentifierExpression(identifier)
        if swizzle is not None:
            left = SwizzleExpression(left, swizzle)

        if binary_op in ["+", "-", "*", "/", "%", "^"]:
            expr = ArithmeticExpression(left, binary_op, right)
        else:
            expr = LogicExpression(left, binary_op, right)

        super().__init__(identifier, swizzle, expr)
