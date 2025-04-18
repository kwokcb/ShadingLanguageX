import re

from .Keyword import KEYWORDS
from .Token import Token
from .token_types import EOF, IDENTIFIER, FLOAT_LITERAL, INT_LITERAL, FILENAME_LITERAL, STRING_LITERAL


def scan(source: str) -> list[Token]:
    scanner = Scanner()
    tokens = scanner.scan(source)
    return tokens


class Scanner:
    def __init__(self):
        self.__source = ""
        self.__index = 0
        self.__line = 1

    def scan(self, source: str) -> list[Token]:
        self.__source = source
        self.__index = 0
        self.__line = 1

        tokens = []
        while self.__index < len(self.__source):
            token = self.__identify_token()
            if token:
                token.__line = self.__line
                tokens.append(token)
                self.__index += len(token.lexeme)
            else:
                self.__line += self.__peek() == "\n"
                self.__index += 1
        tokens.append(self.__token(EOF))
        return tokens

    def __identify_token(self) -> Token | None:
        if self.__is_single_char_token():
            return self.__token(self.__peek())
        if self.__is_compound_token():
            if self.__peek_next() == "=":
                return self.__token(self.__peek() + "=")
            else:
                return self.__token(self.__peek())
        if word := self.__get_word():
            if word in KEYWORDS:
                return self.__token(word)
            else:
                return self.__token(IDENTIFIER, word)
        if float_lit := self.__get_float_literal():
            return self.__token(FLOAT_LITERAL, float_lit)
        if int_lit := self.__get_int_literal():
            return self.__token(INT_LITERAL, int_lit)
        if filename_lit := self.__get_filename_literal():
            return self.__token(FILENAME_LITERAL, filename_lit)
        if string_lit := self.__get_string_literal():
            return self.__token(STRING_LITERAL, string_lit)
        return None

    def __peek(self) -> str | None:
        return self.__source[self.__index] if self.__index < len(self.__source) else None

    def __peek_next(self) -> str | None:
        i = self.__index + 1
        return self.__source[i] if i < len(self.__source) else None

    def __peek_all(self) -> str:
        return self.__source[self.__index:]

    def __is_single_char_token(self) -> bool:
        return self.__peek() in ["(", ")", "{", "}", "[", "]", ".", ",", ":", ";"]

    def __is_compound_token(self) -> bool:
        return self.__peek() in ["!", "=", ">", "<", "+", "-", "*", "/", "%", "^", "&", "|"]

    def __get_word(self) -> str | None:
        match = re.match(r"[_a-zA-Z][_a-zA-Z0-9]*", self.__peek_all())
        return match.group() if match else None

    def __get_float_literal(self) -> str | None:
        match = re.match(r"[0-9]+\.[0-9]+", self.__peek_all())
        return match.group() if match else None

    def __get_int_literal(self) -> str | None:
        match = re.match(r"[0-9]+", self.__peek_all())
        return match.group() if match else None

    def __get_filename_literal(self) -> str | None:
        match = re.match(r'"[^"]*\.(tif|png|jpg)"', self.__peek_all())
        return match.group() if match else None

    def __get_string_literal(self) -> str | None:
        match = re.match(r'"[^"]*"', self.__peek_all())
        return match.group() if match else None

    def __token(self, type_: str, lexeme: str = None) -> Token:
        return Token(type_, lexeme, self.__line)
