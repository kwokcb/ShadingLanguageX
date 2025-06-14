# Version 0.4.1-beta
## Added
Finished implementing standard library functions to match the MaterialX Standard Nodes.

# Version 0.4-beta
## Added
* __Function Overloading__  
Functions can now be overloaded, allowing them to have the same names as long as their signature is unique. In __ShadingLanguageX__, a functions return type is a part of its signature.
```
float length(vec2 v)
{
    return sqrt(v.x * v.x + v.y * v.y);
}

float length(vec3 v)
{
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
}

vec2 uv2 = geompropvalue("uv2");
vec3 n = geompropvalue("Nworld");

float a = length(vv2);
float b = length(n);
```
```
float random()
{
    return randomfloat();
}

vec2 random()
{
    return vec2(randomfloat(), randomfloat());
}

float f = rand();
vec2 v2 = rand();
```
* __Function Templates__  
Templates allow functions with different data types but the same logic to be implemented in a single function.
```
T frac<float, vec2, vec3, vec4, color3, color4>(T value)
{
    return value % 1.0;
}

float a = 0.7;
vec2 v2 = vec2(1.5, 8.1);
color3 c3 = color3(3.4, 0.1, 9.9);

a = frac(a);
v2 = frac(v2);
c3 = frac(c3);
```
In the previous example, the template type `T` was inferred from the functions usage, but it can be specified if the usage is ambiguous or for code clarity.
```
a = frac<float>(a);
v2 = frac<vec2>(v2);
c3 = frac<color3>(c3);
```
The template type `T` can be used wherever a standard data type could have been used inside the function.
```
T image_mult<vec3, color3>(filename img_path, T mult = T(1.0))
{
    T img = image<T>(img_path);
    return img * mult;
}

color3 brick = image_mult("brick.png", color3(0.8, 0.1, 0.1));
vec3 normal = image_mult("brick_normals.png");
```
* __Default Arguments__  
Function parameters can now have default arguments.
```
float incr(float value, float amount=1.0)
{
    return value + amount;
}

float a = 1.0;
a = incr(a);
a = incr(a, 2.0);
```
* __Null Value__  
Any variable can now be assigned the `null` value. When that variable is compiled and its value assigned to the input of a MaterialX node, the input will not be set. This variable can be used anywhere an expression can be evaluated, but is specifically useful to provide default arguments to functions that do not create inputs in the underlying MaterialX nodes, letting MaterialX define the default value instead of the developer.
```
color3 image(filename file, vec2 texcoord = null)
{
    return {"image", color3: file=file, texcoord=texcoord);
}

color3 c = image("butterfly1.png");
```
* __Named Arguments__  
When calling a function, arguments can be named to target specific parameters.
```
color3 image(filename file, color3 default = null, vec2 texcoord = null)
{
    return {"image", color3: file=file, default=default, texcoord=texcoord);
}

color3 c = image("butterfly1.png", texcoord=geompropvalue("uv2"));
```
# Version 0.3-beta
## Added
* __Expression Statements__  
Allow function and standard library calls to be invoked without assigning the returned value. 
```
vec2 uv = texcoord();
displacement(tangent("object"), uv.x * uv.y);
```
* __Preprocessor Directives__  
C-style preprocessor directives that can control the compilation of the shader.
```
#define USE_SRGB
#define GAMMA 2.2
color3 c = image("albedo.png");
#ifdef USE_SRGB
c ^= GAMMA;
#endif
```
* __Ternary Relational Expression__  
Concise expression for checking if an expression falls within a lower and upper limit.
```
bool is_normalized = -1.0 < x < 1.0;
```
* __Improved Main Function__  
Main function name and arguments can now optionally be specified when calling `mxslc.compile_file(...)`.
```
mxslc.compile_file("my_shader.mxsl", main_function="my_function", main_args=[42, 10.0, Path("butterfly1.png")])
```
```
void my_function(int seed, float n, filename img_path)
{
    float y = 0.0;
    for (float i = 0.0 : n)
    {
        y += randomfloat(i, seed=seed);
    }

    vec2 uv = vec2(texcoord().x, y / n);
    surfaceshader surface = standard_surface();
    surface.base_color = image(img_path, texcoord=uv);
}
```
* __Additional Compile Arguments__  
Added several compile arguments to `mxslc.compile_file(...)` and mxslc executable.
```
positional arguments:
  mxsl_path                        Input path to mxsl file or containing folder

options:
  -h, --help                       show this help message and exit
  -o, --output-path OUTPUT_PATH    Output path of generated mtlx file or containing folder
  -m, --main-func MAIN_FUNC        Name of main entry function into the program
  -a, --main-args MAIN_ARGS        Arguments to be passed to the main function
  -i, --include-dirs INCLUDE_DIRS  Additional directories to search when including files
  -d, --define MACROS              Additional macro definitions
```
# Version 0.2-beta
## Added 
* __Node Constructor__  
Manually define a MaterialX nodes category, type and inputs.  
```
vec3 n = image("normals.png");
vec3 v = {"normalmap", vec3: in=n, space="tangent", scale=0.1};
```
###
* __Include Directive__  
Specify other files to be included in compilation.
```
#include "some_functions.mxsl"
```
###
* __Indexer Expression__  
Extract vector and color channels using square brackets.
```
vec3 n = normal();
float x = n[0];
```
###
* __Displacement Shader Support__
```
float height = image("heightmap.png");
displacementshader ds = displacement(tangent(), height);
```
# Version 0.1-beta
## Supported Features
* __Variable Declaration__
* __Variable Assignment__
* __Compound Assignment__
* __Function Declaration__
* __For Loop__
* __Binary Operators__
* __Unary Operators__
* __Grouped Expression__
* __Constructors__
* __Explicit Conversions__
* __Standard Library Calls__
* __User-defined Function Calls__
* __Swizzle Operator__
* __If Expression__
* __Surface Shader Output__
