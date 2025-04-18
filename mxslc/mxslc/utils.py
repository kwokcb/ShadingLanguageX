import re
from typing import Sequence, Generator, Any

from .Keyword import FLOAT, VECTOR2, VECTOR3, VECTOR4, COLOR3, COLOR4, DataType


def type_of_swizzle(swizzle: str) -> DataType:
    is_vector_swizzle = re.match(r"[xyzw]", swizzle)
    if len(swizzle) == 1:
        return FLOAT
    if len(swizzle) == 2:
        return VECTOR2
    if len(swizzle) == 3:
        return VECTOR3 if is_vector_swizzle else COLOR3
    if len(swizzle) == 4:
        return VECTOR4 if is_vector_swizzle else COLOR4
    raise AssertionError


def as_list(value: Any) -> list[Any] | None:
    if value is None:
        return None
    elif isinstance(value, list):
        return value
    else:
        return [value]


def one(values: Sequence[bool] | Generator[bool, None, None]) -> bool:
    return len([v for v in values if v]) == 1


# TODO make this more robust
def is_path(literal: Any) -> bool:
    if not isinstance(literal, str):
        return False
    return literal.endswith(".tif") or literal.endswith(".png") or literal.endswith(".jpg")
