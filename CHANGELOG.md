# Version 0.3-beta (in development)
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
