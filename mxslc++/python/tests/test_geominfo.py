import mxslc


MTLX_WITH_GEOMINFO = """<?xml version="1.0"?>
<materialx version="1.38">
  <image name="image_color" type="color3">
    <input name="file" type="filename" value="resources/Images/grid_udim/grid.<UDIM>.png" colorspace="srgb_texture" />
  </image>
  <geominfo name="cube_geom" geom="/">
    <geomprop name="udimset" type="stringarray" value="1001, 1002, 1003, 1011, 1012, 1013" />
  </geominfo>
  <standard_surface name="cube_shader" type="surfaceshader">
    <input name="base_color" type="color3" nodename="image_color" />
  </standard_surface>
  <surfacematerial name="cube_material" type="material">
    <input name="surfaceshader" type="surfaceshader" nodename="cube_shader" />
  </surfacematerial>
</materialx>
"""


def test_decompile_emits_geominfo_statement():
    result = mxslc.decompile_string_to_string(MTLX_WITH_GEOMINFO)

    assert 'geominfo("cube_geom", "/")' in result
    assert 'geomprop("udimset", "stringarray", "1001, 1002, 1003, 1011, 1012, 1013");' in result


MXSL_WITH_GEOMINFO = """geominfo("cube_geom", "/")
{
    geomprop("udimset", "stringarray", "1001, 1002, 1003, 1011, 1012, 1013");
}
color3 image_color = image(@colorspace "srgb_texture" file = "resources/Images/grid_udim/grid.<UDIM>.png");
surfaceshader cube_shader = standard_surface(base_color = image_color);
material cube_material = surfacematerial(surfaceshader = cube_shader);
"""


def test_compile_emits_geominfo_element():
    result = mxslc.compile_string_to_string(MXSL_WITH_GEOMINFO)

    assert '<geominfo name="cube_geom" geom="/">' in result
    assert '<geomprop name="udimset" type="stringarray" value="1001, 1002, 1003, 1011, 1012, 1013" />' in result
