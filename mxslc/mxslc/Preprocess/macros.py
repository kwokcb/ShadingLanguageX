from ..Token import Token
from ..scan import as_token

_macros: list[tuple[Token, list[Token]]] = []


def define(identifier: str | Token, value: list[Token] = None) -> None:
    identifier = as_token(identifier)
    if is_defined(identifier):
        # TODO add warning when defining a defined macro
        undefine(identifier)
    _macros.append((identifier, value or []))


def undefine(identifier: str | Token) -> None:
    identifier = as_token(identifier)
    for macro in _macros:
        if macro[0] == identifier:
            _macros.remove(macro)
            return
    # TODO add warning when undefining an undefined macro


def is_defined(identifier: str | Token) -> bool:
    identifier = as_token(identifier)
    return identifier in [m[0] for m in _macros]


def replace(identifier: str | Token) -> list[Token]:
    identifier = as_token(identifier)
    for macro in _macros:
        if macro[0] == identifier:
            return macro[1]
    raise AssertionError()


def clear() -> None:
    _macros.clear()
