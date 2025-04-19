from pathlib import Path

import pytest

import mxslc

_overwrite_all_expected = False


@pytest.mark.parametrize("filename, overwrite_expected", [
    ("interiormapping_room", False),
    ("interiormapping_words", False),
    ("redbrick", False),
    ("shaderart", False),
    ("condensation", False),
    ("binary_expressions", False),
    ("for_loops_1", False),
    ("for_loops_2", False),
    ("for_loops_3", False),
    ("for_loops_4", False),
    ("for_loops_5", False),
    ("named_arguments_1", False),
    ("named_arguments_2", False),
])
def test_mxslc(filename: str, overwrite_expected: bool) -> None:
    mxsl_path = (Path(__file__).parent / "data" / "mxsl" / filename).with_suffix(".mxsl")
    with open(mxsl_path, "r") as f:
        code = f.read()

    actual_xml = mxslc.compile_string(code)

    mtlx_path = (Path(__file__).parent / "data" / "mtlx" / filename).with_suffix(".mtlx")
    if overwrite_expected or _overwrite_all_expected:
        with open(mtlx_path, "w") as f:
            f.write(actual_xml)
    else:
        with open(mtlx_path, "r") as f:
            expected_xml = f.read()
        # replace slashes to work on both windows and linux
        assert actual_xml.replace("\\", "/") == expected_xml.replace("\\", "/")
