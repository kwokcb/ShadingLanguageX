from .Argument import Argument
from .CompileError import CompileError
from .Expressions import *
from .Keyword import DATA_TYPES, Keyword
from .Parameter import Parameter
from .StandardLibrary import StandardLibrary
from .Statements import *
from .Token import Token
from .token_types import EOF, IDENTIFIER, FLOAT_LITERAL, INT_LITERAL, STRING_LITERAL, FILENAME_LITERAL


def parse(tokens: list[Token]) -> list[Statement]:
    parser = Parser()
    statements = parser.parse(tokens)
    return statements


class Parser:
    def __init__(self):
        self.tokens: list[Token] = []
        self.index = 0

    def parse(self, tokens: list[Token]) -> list[Statement]:
        self.tokens = tokens
        self.index = 0
        return self.__program()

    def __program(self) -> list[Statement]:
        statements = []
        while self.__peek() != EOF:
            statements.append(self.__statement())
        return statements

    def __statement(self) -> Statement:
        token = self.__peek()
        if token in DATA_TYPES:
            return self.__declaration()
        if token == IDENTIFIER:
            return self.__assignment()
        if token == Keyword.FOR:
            return self.__for_loop()
        raise CompileError(token.line, f"Expected return statement, data type keyword, identifier or 'for', but found '{token.lexeme}'.")

    def __declaration(self) -> Statement:
        data_type = self.__match(*DATA_TYPES)
        identifier = self.__match(IDENTIFIER)
        token = self.__peek()
        if token == "=":
            return self.__variable_declaration(data_type, identifier)
        if token == "(":
            return self.__function_declaration(data_type, identifier)
        raise CompileError(token.line, f"Expected '=' or '(', but found '{token.lexeme}'.")

    def __variable_declaration(self, data_type: Token, identifier: Token) -> VariableDeclaration:
        self.__match("=")
        right = self.__expression()
        self.__match(";")
        return VariableDeclaration(data_type, identifier, right)

    def __function_declaration(self, data_type: Token, identifier: Token) -> FunctionDeclaration:
        self.__match("(")
        if self.__consume(")"):
            params = []
        else:
            params = [self.__parameter()]
            while self.__consume(","):
                params.append(self.__parameter())
            self.__match(")")
        self.__match("{")
        statements = []
        while self.__peek() != Keyword.RETURN:
            statements.append(self.__statement())
        self.__match(Keyword.RETURN)
        return_expr = self.__expression()
        self.__match(";")
        self.__match("}")
        return FunctionDeclaration(data_type, identifier, params, statements, return_expr)

    def __parameter(self) -> Parameter:
        data_type = self.__match(*DATA_TYPES)
        identifier = self.__match(IDENTIFIER)
        return Parameter(identifier, data_type)

    def __assignment(self) -> Statement:
        identifier = self.__match(IDENTIFIER)
        property = self.__match(IDENTIFIER) if self.__consume(".") else None
        token = self.__peek()
        if token == "=":
            return self.__variable_assignment(identifier, property)
        if token in ["+=", "-=", "*=", "/=", "%=", "^=", "&=", "|="]:
            return self.__compound_assignment(identifier, property)
        raise CompileError(token.line, f"Unexpected token: '{token.lexeme}'.")

    def __variable_assignment(self, identifier: Token, property: Token) -> VariableAssignment:
        self.__match("=")
        right = self.__expression()
        self.__match(";")
        return VariableAssignment(identifier, property, right)

    def __compound_assignment(self, identifier: Token, property: Token) -> CompoundAssignment:
        operator = self.__match("+=", "-=", "*=", "/=", "%=", "^=", "&=", "|=")
        right = self.__expression()
        self.__match(";")
        return CompoundAssignment(identifier, property, operator, right)

    def __for_loop(self) -> ForLoop:
        self.__match(Keyword.FOR)
        self.__match("(")
        data_type = self.__match(*DATA_TYPES)
        identifier = self.__match(IDENTIFIER)
        self.__match("=")
        literal1 = self.__match(FLOAT_LITERAL, IDENTIFIER)
        self.__match(":")
        literal2 = self.__match(FLOAT_LITERAL, IDENTIFIER)
        if self.__consume(":"):
            literal3 = self.__match(FLOAT_LITERAL, IDENTIFIER)
        else:
            literal3 = None
        self.__match(")")
        self.__match("{")
        statements = []
        while self.__peek() != "}":
            statements.append(self.__statement())
        self.__match("}")
        return ForLoop(data_type, identifier, literal1, literal2, literal3, statements)

    def __expression(self) -> Expression:
        return self.__logic()

    def __logic(self) -> Expression:
        expr = self.__equality()
        while op := self.__consume("&", Keyword.AND, "|", Keyword.OR):
            right = self.__equality()
            expr = LogicExpression(expr, op, right)
        return expr

    def __equality(self) -> Expression:
        expr = self.__relational()
        while op := self.__consume("!=", "=="):
            right = self.__relational()
            expr = ComparisonExpression(expr, op, right)
        return expr

    def __relational(self) -> Expression:
        expr = self.__term()
        while op := self.__consume(">", ">=", "<", "<="):
            right = self.__term()
            expr = ComparisonExpression(expr, op, right)
        return expr

    def __term(self) -> Expression:
        expr = self.__factor()
        while op := self.__consume("+", "-"):
            right = self.__factor()
            expr = ArithmeticExpression(expr, op, right)
        return expr

    def __factor(self) -> Expression:
        expr = self.__exponent()
        while op := self.__consume("*", "/", "%"):
            right = self.__exponent()
            expr = ArithmeticExpression(expr, op, right)
        return expr

    def __exponent(self) -> Expression:
        expr = self.__unary()
        while op := self.__consume("^"):
            right = self.__unary()
            expr = ArithmeticExpression(expr, op, right)
        return expr

    def __unary(self) -> Expression:
        if op := self.__consume("!", Keyword.NOT, "+", "-"):
            return UnaryExpression(op, self.__swizzle())
        else:
            return self.__swizzle()

    def __swizzle(self) -> Expression:
        expr = self.__primary()
        if self.__consume("."):
            swizzle = self.__match(IDENTIFIER)
            return SwizzleExpression(expr, swizzle)
        else:
            return expr

    def __primary(self) -> Expression:
        # literal
        if literal := self.__consume(Keyword.TRUE, Keyword.FALSE, INT_LITERAL, FLOAT_LITERAL, STRING_LITERAL, FILENAME_LITERAL):
            return LiteralExpression(literal)
        # grouping
        if self.__consume("("):
            expr = self.__expression()
            self.__match(")")
            return GroupingExpression(expr)
        # stdlib call / function call / identifier
        if identifier := self.__consume(IDENTIFIER):
            if self.__peek() == "(":
                # stdlib call
                if identifier.lexeme in StandardLibrary:
                    return self.__standard_library_call(identifier)
                # function call
                else:
                    return self.__function_call(identifier)
            # identifier
            else:
                return IdentifierExpression(identifier)
        token = self.__peek()
        # constructor call
        if token in DATA_TYPES:
            return self.__constructor_call()
        # if
        if token == Keyword.IF:
            return self.__if_expression()
        # switch
        if token == Keyword.SWITCH:
            return self.__switch_expression()
        raise CompileError(token.line, f"Unexpected token: '{token}'.")

    def __if_expression(self) -> Expression:
        self.__match(Keyword.IF)
        self.__match("(")
        clause = self.__expression()
        self.__match(")")
        self.__match("{")
        then = self.__expression()
        self.__match("}")
        if self.__consume(Keyword.ELSE):
            self.__match("{")
            otherwise = self.__expression()
            self.__match("}")
        else:
            otherwise = None
        return IfExpression(clause, then, otherwise)

    def __switch_expression(self) -> Expression:
        self.__match(Keyword.SWITCH)
        self.__match("(")
        which = self.__expression()
        self.__match(")")
        self.__match("{")
        values = [self.__expression()]
        while self.__consume(","):
            values.append(self.__expression())
        self.__match("}")
        return SwitchExpression(which, values)

    def __constructor_call(self) -> Expression:
        data_type = self.__match(*DATA_TYPES)
        self.__match("(")
        if self.__consume(")"):
            args = []
        else:
            args = [self.__argument()]
            while self.__consume(","):
                args.append(self.__argument())
            self.__match(")")
        return ConstructorCall(data_type, args)

    def __standard_library_call(self, identifier: Token) -> Expression:
        self.__match("(")
        if self.__consume(")"):
            args = []
        else:
            args = [self.__argument()]
            while self.__consume(","):
                args.append(self.__argument())
            self.__match(")")
        return StandardLibraryCall(identifier, args)

    def __function_call(self, identifier: Token) -> Expression:
        self.__match("(")
        if self.__consume(")"):
            args = []
        else:
            args = [self.__argument()]
            while self.__consume(","):
                args.append(self.__argument())
            self.__match(")")
        return FunctionCall(identifier, args)

    def __argument(self) -> Argument:
        if self.__peek() == IDENTIFIER and self.__peek_next() == "=":
            name = self.__match(IDENTIFIER)
            self.__match("=")
        else:
            name = None
        return Argument(self.__expression(), name)

    def __peek(self) -> Token:
        """
        Peek next token.
        """
        return self.tokens[self.index]

    def __peek_next(self) -> Token:
        """
        Peek next next token.
        """
        return self.tokens[self.index + 1]

    def __consume(self, *token_types: str) -> Token | None:
        """
        Consume next token if it matches one of the token types.
        """
        token = self.__peek()
        if token in token_types:
            self.index += 1
            return token
        return None

    def __match(self, *token_types: str) -> Token:
        """
        Same as consume, but raise a compile error if no match was found.
        """
        if token := self.__consume(*token_types):
            return token
        token = self.__peek()
        raise CompileError(token.line, f"Expected {token_types}, but found '{token.lexeme}'.")
