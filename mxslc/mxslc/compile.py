from . import mtlx
from .Statements import Statement


def compile(statements: list[Statement]) -> str:
    for statement in statements:
        statement.execute()
    return mtlx.get_xml()
