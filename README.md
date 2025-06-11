
<h1 align="center">ShadingLanguageX</h1>

__ShadingLanguageX__ is a high level programming language that can be used to create complex MaterialX shaders.  
  
![](examples/screenshots/readme_example.png)


# How It Works
![](examples/screenshots/howitworks.jpg)  

__ShadingLanguageX__ source files are compiled to MaterialX (.mtlx) files using the mxslc compiler. Internally, the source file is tokenized and parsed into a list of statements and expressions which in turn map to one or more MaterialX nodes. These nodes are then written to the MaterialX output file as shown in the diagram above.  
For example, the `+` operator (e.g., `float x = 1.0 + 1.0;`) intuitively compiles to the `add` node, and the same for all other mathematical operators. `if` expressions compile to either of the `ifgreater`, `ifgreatereq` or `ifequal` nodes depending on the condition. `switch` expressions compile to the `switch` node. The swizzle operator (e.g., `some_vector.xy`) compiles to `extract` and `combine` nodes. Most MaterialX nodes are represented by a standard library function that is built into the language, such as `color3 c = image("albedo.png");` which compiles to the `image` node. Additionally, declaring a variable (e.g., `vec3 up = vec3(0, 1, 0);`) compiles to a `constant` node (or a `combine` node depending on the inputs to the expression).  


# Why Use ShaderLanguageX? ---(Merge subsections into one paragraph)---

Currently, MaterialX shaders can be made either using the MaterialX C++ or Python APIs, or using a node editor software. __ShadingLanguageX__ provides several benefits over these existing methods.

#### Manage Complexity

Using existing methods, it can be difficult to develop and maintain complex MaterialX shaders with many nodes. __ShadingLanguageX__ provides a concise syntax and tools such as for loops and user-defined functions that make it easy to develop complex shaders.

#### Reuse Functionality

__ShadingLanguageX__ supports the `#include` directive that make it easy to reuse code in more than one project. 

#### Iterate Quickly

The MaterialX API can be quite verbose to use when writing shaders because it needs to provide control over every aspect of MaterialX. Developers can write their own wrappers around the API, but this takes time and knowledge about either C++ or Python. __ShadingLanguageX__ has a less functionality than the MaterialX API, but in return provides a language with a simple syntax, a much smaller syntax grammar to learn, and one that was developed specifically for building MaterialX shaders. There is no setup code to write, just the shaders and a call to the compiler.

#### Code Readability

TODO

# Getting Started

## Installation
__ShadingLanguageX__ source files are compiled to MaterialX (.mtlx) files using its open source compiler (mxslc). The compiler is written in python and can be cloned or downloaded as a package and called from your own python project. It has been tested with Python 3.12 and 3.13. 
```python
import mxslc
mxslc.compile_file("concrete.mxsl")
```
Alternatively, you can download the compiler executable from the most recent release and call it from the command line.
```
> ./mxslc.exe concrete.mxsl
```
Both examples will output a `concrete.mtlx` file which can then be used as you would any other MaterialX file. Both methods have the same input signature, a mandatory path to a __ShadingLanguageX__ source file and then several optional arguments, such as setting the output files directory and name.

## ShadingLanguageX - Hello World
```
// hello_world.mxsl
void hello_world(filename albedo_file)
{
    surfaceshader surface = standard_surface();
    surface.base_color = image(albedo_file);
}
```
Compile using python:
```python
from pathlib import Path
import mxslc
mxslc.compile_file("hello_world.mxsl", main_func="hello_world", main_args=[Path("textures/albedo.png")]);
```
or executable:
```
> ./mxslc.exe hello_world.mxsl -m hello_world -a textures/albedo.png
```
Output: hello_world.mtlx
```xml
<?xml version="1.0"?>
<materialx version="1.39">
  <standard_surface name="hello_world__surface" type="surfaceshader">
    <input name="base_color" type="color3" nodename="node1" />
  </standard_surface>
  <image name="node1" type="color3">
    <input name="file" type="filename" value="textures\albedo.png" />
  </image>
  <surfacematerial name="mxsl_material" type="material">
    <input name="surfaceshader" type="surfaceshader" nodename="hello_world__surface" />
  </surfacematerial>
</materialx>
```

## Language Specification
For information regarding __ShadingLanguageX__ syntax and mxslc compiler options, see the __ShadingLanguageX__ [language specification](https://github.com/jakethorn/ShadingLanguageX/blob/main/docs/LanguageSpecification.md). Additionally, more examples can be found [here](https://github.com/jakethorn/ShadingLanguageX/tree/main/examples).

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
