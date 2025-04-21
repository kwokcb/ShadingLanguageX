# Version 0.2-beta (in development)
## Added 
* __Node Constructor__  
Manually define a MaterialX nodes category, type and inputs.  
```
vec3 n = image("normals.png");
vec3 v = {"normalmap", vec3: in=n, space="tangent", scale=0.1};
```
* __Include Directive__  
Specify other files to be included in compilation.
```
#include "some_functions.mxsl"
```
* __Indexer Expression__  
Extract vector and color channels using square brackets.
```
vec3 n = normal();
float x = n[0];
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
