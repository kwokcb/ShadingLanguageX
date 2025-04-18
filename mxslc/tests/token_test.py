from pathlib import Path

import pytest

from mxslc.scan import scan
from mxslc.token_types import FILENAME_LITERAL


@pytest.mark.parametrize("path", ["C:/image.png", "C:\\image.png", "./image.png", ".\\image.png", "../image.png", "..\\image.png"])
def test_path_token(path):
    tokens = scan(f'filename path = "{path}";')
    path_token = tokens[-3]
    assert path_token == FILENAME_LITERAL
    assert isinstance(path_token.value, Path)


def test_path_with_single_backslash():
    with open(Path(__file__).parent / "data" / "test_filename.mxsl", "r") as f:
        code = f.read()
    tokens = scan(code)
    path_token = tokens[-8]
    assert path_token == FILENAME_LITERAL
    assert isinstance(path_token.value, Path)
    assert str(path_token.value) == r"C:\Users\jaket\PycharmProjects\mxsl\data\textures\cinderTiles_001_001_010_albedo.tif";
    path_token = tokens[-3]
    assert path_token == FILENAME_LITERAL
    assert isinstance(path_token.value, Path)
    assert str(path_token.value) == r"C:\newfolder\niceimage.tif";
