[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/jakethorn/MXSL/blob/main/LICENSE)
[![Version](https://img.shields.io/github/v/release/jakethorn/MXSL)](https://github.com/jakethorn/MXSL/releases/latest)
[![Build Status](https://github.com/jakethorn/MXSL/workflows/automated-tests/badge.svg)](https://github.com/jakethorn/MXSL/actions)

# ShadingLanguageX
__ShadingLanguageX__ is a high level shading language that can be used to create complex MaterialX materials.  
  
![](examples/screenshots/readme_example.png)


# How It Works
![](examples/screenshots/howitworks.jpg)  

__ShadingLanguageX__ source files are compiled to MaterialX (.mtlx) files using the mxslc compiler. Internally, the source file is tokenized and parsed into a list of statements and expressions which in turn map to one or more MaterialX nodes. These nodes are then written to the MaterialX output file as shown in the diagram above.  
For example, the `+` operator (e.g., `float x = 1.0 + 1.0;`) intuitively compiles to the `add` node, and the same for all other mathematical operators. `if` expressions compile to either of the `ifgreater`, `ifgreatereq` or `ifequal` nodes depending on the condition. `switch` expressions compile to the `switch` node. The swizzle operator (e.g., `some_vector.xy`) compiles to `extract` and `combine` nodes. Most MaterialX nodes are represented by a standard library function that is built into the language, such as `color3 c = image("albedo.png");` which compiles to the `image` node. Additionally, declaring a variable (e.g., `vec3 up = vec3(0, 1, 0);`) compiles to a `constant` node (or a `combine` node depending on the inputs to the expression).  


# Getting Started

## Installation
__ShadingLanguageX__ source files are compiled to MaterialX (.mtlx) files using its open source compiler (mxslc). The compiler is written in python and can be cloned or downloaded as a package and called from your own python project. Works with Python 3.12 and 3.13. 
```python
import mxslc
mxslc.compile_file("grass.mxsl")
```
Alternatively, you can download the compiler executable from the most recent release and call it from the command line.
```
./mxslc.exe grass.mxsl
```
Both methods will output a `grass.mtlx` file which can then be used as you would any other MaterialX file. Both methods also have the same input signature, a mandatory path to a __ShadingLanguageX__ source file and then several optional arguments, such as setting the output files directory and name.

## Language Specification
__ShadingLanguageX__ is a high level shading with a syntax similar to C. There are additional data types like `vector2`, `vector3`, `vector4`, `color3` and `color4` that match those from the MaterialX specification. Vectors also have the aliases `vec2`, `vec3` and `vec4`. The language also supports preprocessor directives like `#include`, `#if`, `#define` and others. It, however, does not support true control flow. If statements are replaced with if expressions and for loops must have a constant terminator. It comes with a built-in standard library of functions which is equivalent to the standard nodes found in the MaterialX specification found [here](https://github.com/AcademySoftwareFoundation/MaterialX/blob/main/documents/Specification/MaterialX.StandardNodes.md). Function parameters are one-to-one with their corresponding nodes inputs.
  
For more information about __ShadingLanguageX__ syntax and additional compiler options, see the [language specification](https://github.com/jakethorn/ShadingLanguageX/blob/main/language-spec/LanguageSpecification_v0_3-beta.md).  
  
You can also look through example source files [here](https://github.com/jakethorn/ShadingLanguageX/tree/main/examples) to see uses of __ShadingLanguageX__.

## Interactive Compiler (Experimental)
The python installation also comes with an interactive compiler which allows the user to call __ShadingLanguageX__ functions and access variables from python. This is useful if more complex logic is needed when compiling the shader, such as checking for missing textures files, or updating values or logic based on a configuration file.
For example:
```
color3 logic_1(filename texture_path)
{
    // some logic here
}

color3 logic_2(color3 c)
{
    // some other logic here
}

void main(color3 c)
{
    standard_surface(base_color=c);
}
```
```python
from pathlib import Path
import MaterialX as mx
import mxslc

compiler = mxslc.InteractiveCompiler()
compiler.include(Path("./my_shader.mxsl")

shader = compiler.get_shader_interface()
texture_path = Path("../textures/my_texture.png")
if texture_path.exists():
    c = shader.logic_1(texture_path)
else:
    c = shader.logic_2(mx.Color3(1, 0, 0))
shader.main(c)

compiler.save(Path("./my_shader.mtlx"))
```


# Examples
Red Brick                    |  Interior Mapping
:---------------------------:|:---------------------------:
![](examples/screenshots/redbrick.png)   |  ![](examples/screenshots/interiormapping.png)
__Shader Art (by Kishimisu)__    |  __Interior Mapping with shadows (by VRBN)__
![](examples/screenshots/shaderart.png)  |  ![](examples/screenshots/lit_interiors.png)
__Displacement Mountain__    |    __Procedural Rain__
![](examples/screenshots/mountain.png)   |  ![](examples/screenshots/rain.png)

# Contributing
Please try out __ShadingLanguageX__ and start a discussion about a feature you'd like to see or an issue if you find a bug, or feel free to contribute directly to the project by opening a pull request!
