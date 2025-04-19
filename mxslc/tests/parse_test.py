from pathlib import Path

from mxslc import mtlx, state
from mxslc.compile import _compile
from mxslc.parse import parse
from mxslc.scan import scan


def _get_code_and_expected(stem: str) -> tuple[str, str]:
    data_folder = Path(__file__).parent / "data"
    with open(data_folder / "mxsl" / f"{stem}.mxsl", "r") as f:
        mxsl = f.read()
    with open(data_folder / "mtlx" / f"{stem}.mtlx", "r") as f:
        mtlx = f.read()
    return mxsl, mtlx


def _assert_data_file(stem: str) -> None:
    mtlx.clear()
    state.clear()
    code, expected = _get_code_and_expected(stem)
    tokens = scan(code)
    statements = parse(tokens)
    _compile(statements)
    assert mtlx.get_xml().replace("\\", "/") == expected.replace("\\", "/")


def test_parse_with_examples():
    _assert_data_file("test_001")
    _assert_data_file("test_002")
    _assert_data_file("test_003")
    _assert_data_file("test_004")
    _assert_data_file("test_005")
    _assert_data_file("test_006")
    _assert_data_file("test_007")
    _assert_data_file("test_008")
    _assert_data_file("test_009")
    _assert_data_file("test_010")
