import mxslc
import pytest

UPSTREAM_SHADER_OUTPUT = """<?xml version="1.0"?>
<materialx version="1.39">
  <gltf_pbr name="gltf_mat" type="surfaceshader" />
  <surfacematerial name="Default" type="material">
    <input name="surfaceshader" type="surfaceshader" nodename="gltf_mat" />
  </surfacematerial>
</materialx>
"""

EMPTY_STRING_SHADER_OUTPUT = """<?xml version="1.0"?>
<materialx version="1.39">
  <gltf_pbr name="gltf_mat" type="surfaceshader" />
  <surfacematerial name="Default" type="material">
    <input name="surfaceshader" type="surfaceshader" nodename="gltf_mat" />
    <input name="backsurfaceshader" type="surfaceshader" value="" />
    <input name="displacementshader" type="displacementshader" value="" />
  </surfacematerial>
  <volumematerial name="VolumeMaterial" type="material">
    <input name="volumeshader" type="volumeshader" value="" />
  </volumematerial>
</materialx>
"""


def test_shader_input_accepts_upstream_shader():
    source = (
        "surfaceshader gltf_mat = gltf_pbr();\n"
        "material Default = surfacematerial(surfaceshader = gltf_mat);"
    )

    result = mxslc.compile_string_to_string(source)

    assert isinstance(result, str)
    assert result == UPSTREAM_SHADER_OUTPUT


def test_shader_input_accepts_empty_string():
    source = (
        "surfaceshader gltf_mat = gltf_pbr();\n"
        'material Default = surfacematerial(surfaceshader = gltf_mat, backsurfaceshader = "", displacementshader = "");'
        'material VolumeMaterial = volumematerial(volumeshader = "");'
    )

    result = mxslc.compile_string_to_string(source)

    assert isinstance(result, str)
    assert result == EMPTY_STRING_SHADER_OUTPUT


def test_shader_input_rejects_non_empty_string():
    source = 'material my_main() { return surfacematerial(displacementshader = "non_empty_string"); }'

    with pytest.raises(
        RuntimeError,
        match="Attempting to assign an expression of type string to a variable or parameter of type displacementshader",
    ):
        mxslc.compile_string_to_string(source)


def test_shader_input_rejects_mismatched_shader_type():
    source = "material my_main() { return surfacematerial(displacementshader = gltf_pbr()); }"

    with pytest.raises(
        RuntimeError,
        match="Matching definition could not be found for function 'surfacematerial'",
    ):
        mxslc.compile_string_to_string(source)
