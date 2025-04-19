__Variable Declaration__
```
float f = 1.0;
```
__Variable Assignment__
```
f = 2.0;
```
__Compound Assignment__
```
f *= 3.0;
```
__Function Declaration__
```
color3 linearize(color3 c)
{
    return c ^ 2.2;
}
```
__For Loops__
```
for (float i = 0.0 : 10.0)
{
    // do something with i...
}
```
__Binary Operators__
```
float x = 1.0 + 2.0 - 3.0 * 4.0 / 5.0;
```
__Unary Operators__
```
float y = -x;
```
__Grouped Expressions__
```
float z = (y + 2.0) * 0.5;
```
__Constructors__
```
vec3 my_vec3 = vec3(1, 0, 0);
```
__Explicit Conversions__
```
vec4 my_vec4 = vec4(my_vec3);
```
__Standard Library Calls__
```
vec2 uv = texcoord();
color3 background = image("textures/skyline.png", texcoord=uv);
```
__User-defined Function Calls__
```
background = linearize(background);
```
__Swizzle Operator__
```
float red = background.r;
float blue = background.b;
float green = background.g;
color3 color_shifted = background.gbr;
```
__If Expressions__
```
color3 out_color = if (uv.x < 0.5) { background } else { color_shifted };
```
__Surface Shader Output__
```
surfaceshader surface = standard_surface();
surface.base_color = out_color;
```
