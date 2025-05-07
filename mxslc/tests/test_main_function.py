from pathlib import Path

import MaterialX as mx
import pytest

import mxslc

_overwrite_all_expected = False


@pytest.mark.parametrize("filename, main_function, main_args, overwrite_expected", [
    ("main_function/main_function_1", None, [], False),
    ("main_function/main_function_2", None, [], False),
    ("main_function/main_function_3", "_main", [], False),
    ("main_function/main_function_4", "_main", [], False),
    ("main_function/main_function_5", None, [], False),
    ("main_function/main_function_6", None, [0.2, 0.5, 0.8], False),
    ("main_function/main_function_7", None, [1.0, Path("butterfly1.png")], False),
    ("main_function/main_function_8", "my_function", [mx.Vector2(), mx.Color3(1.0, 0.0, 0.0)], False),
    ("main_function/main_function_9", None, [], False),
    ("main_function/main_function_10", "main", [], False),
])
def test_mxslc(filename: str, main_function: str | None, main_args: list, overwrite_expected: bool) -> None:
    mxsl_path     = (Path(__file__).parent / "data" / "mxsl" / filename).with_suffix(".mxsl")
    actual_path   = (Path(__file__).parent / "data" / "mxsl" / filename).with_suffix(".mtlx")
    expected_path = (Path(__file__).parent / "data" / "mtlx" / filename).with_suffix(".mtlx")

    if overwrite_expected or _overwrite_all_expected:
        actual_path = expected_path

    mxslc.compile_file(mxsl_path, actual_path, main_function=main_function, main_args=main_args)

    with open(actual_path, "r") as f:
        actual = f.read()

    with open(expected_path, "r") as f:
        expected = f.read()

    if not (overwrite_expected or _overwrite_all_expected):
        actual_path.unlink()

    assert actual.replace("\\", "/") == expected.replace("\\", "/")
