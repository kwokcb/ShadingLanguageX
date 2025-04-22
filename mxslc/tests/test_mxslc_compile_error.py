from pathlib import Path

import pytest

import mxslc
from mxslc.CompileError import CompileError


@pytest.mark.parametrize("filename", [
    "bad_func_name_1",
])
def test_mxslc_compile_error(filename: str) -> None:
    mxsl_path = (Path(__file__).parent / "data" / "error" / filename).with_suffix(".mxsl")
    mtlx_path = (Path(__file__).parent / "data" / "error" / filename).with_suffix(".mtlx")

    with pytest.raises(CompileError):
        mxslc.compile_file(mxsl_path)

    mtlx_path.unlink(missing_ok=True)