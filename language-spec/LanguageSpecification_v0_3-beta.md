# Overview

ShadingLanguageX is a high level shading language that allows developers to write shaders that can be compiled into MaterialX (.mtlx) files.
The primary use case is to provide a method of creating MaterialX shaders without using a node editor or the MaterialX C++ or Python APIs.
Node editors are useful for creating simple material networks, but can become combersome for larger networks. 
At the same time, the MaterialX API can be quite verbose, making it difficult to quickly iterate when writing a shader.
ShadingLanguageX is a simple, yet powerful language for writing complex MaterialX shaders.

A core aim of ShadingLanguageX is to maximize portability. At the time of writing, many renderers and frameworks only support 
a subset of the MaterialX specification. To ensure that ShaderLanguageX is compatible with as many platforms as possible, 
it compiles only to standard node elements. More advanced elements like `<nodedef>` or `<nodegraph>` are not used in ShadingLanguageX
despite being the best choice for statements like function declarations or for loops. As support for MaterialX becomes more
mature and as we continue to work on ShadingLanguageX more features will become utilised.

At the end of the day, ShadingLanguageX is based on the MaterialX specification and we've striven for equavilency as much
as possible. As such, if anything is omitted from this document, you can assume that the behaviour is the same as what is
described in the official MaterialX specification. For example, we don't specify in this document what is the return 
type of a `vector3` multiplied by a `float`, as it is already described in the MaterialX Standard Node [document](https://github.com/AcademySoftwareFoundation/MaterialX/blob/main/documents/Specification/MaterialX.StandardNodes.md). 
This is to keep this document as concise as possible as well as to reduce the chance of needing to update it in the future 
due to changes to the official MaterialX documentation.

# Data Types
Data types match the ones found in the MaterialX [specification](https://github.com/AcademySoftwareFoundation/MaterialX/blob/main/documents/Specification/MaterialX.Specification.md#materialx-data-types), with the expection of arrays, matrices, volumeshader and lightshader.  
  
## Supported Data Types

| Data Type            | Example                       |
|----------------------|-------------------------------|
| `boolean`            | `true` or `false`             |
| `integer`            | `79`                          |
| `float`              | `2.2`                         |
| `vector2`            | `vector2(0.0, 1.0)`           |
| `vector3`            | `vector3(0.0, 1.0, 2.0)`      |
| `vector4`            | `vector4(0.0, 1.0, 2.0, 3.0)` |
| `color3`             | `color3(1.0, 0.0, 0.0)`       |
| `color4`             | `color4(1.0, 0.0, 0.0, 1.0)`  |
| `string`             | `"tangent"`                   |
| `filename`           | `"../textures/albedo.png"`    |
| `surfaceshader`      | `standard_surface()`          |
| `displacementshader` | `displacement()`              |

## Type Aliases

ShadingLanguageX provides the following type aliases. They are functionally equivalent to their underlying type.
In this document I will typically use the aliased version for the sake of brevity.

`boolean` ➔ `bool`  
`integer` ➔ `int`  
`vector2` ➔ `vec2`  
`vector3` ➔ `vec3`  
`vector4` ➔ `vec4`

# Expressions

Expressions are pieces of code that evaluate to a value, such as `1.0 + 1.0`. This document will cover each expression in detail
in its own section. The following table gives a quick overview of all the expressions supported by ShadingLanguageX.

| Expression                  | Example                              |
|-----------------------------|--------------------------------------|
| Binary Operator             | `a / b`                              |
| Unary Operator              | `-a`                                 |
| Ternary Relational Operator | `x < a < y`                          |
| Swizzle Operator            | `a.xy`                               |
| Indexing Operator           | `a[0]`                               |
| Literal                     | `3.14`                               |
| Identifier                  | `a`                                  |
| Grouping Expression         | `(a + b)`                            |
| If Expression               | `if (a < b) { x } else { y }`        |
| Switch Expression           | `switch (a) { x, y, z }`             |
| Function Call               | `my_function(a, b)`                  |
| Standard Library Call       | `image("albedo.png", texcoord=uv)`   |
| Constructor Call            | `vec3()`                             |
| Node Constructor            | `{"mix", color3: bg=a, fg=b, mix=c}` |

# Statements

Statements are pieces of code that change the state of the program, either by storing a named variable or function so it
can be accessed later or by controlling the flow of the program. Statements are typically termined with the semicolon `;`. 
This document will cover each statement in detail in its own section. The following table gives a quick overview of all 
the statements supported by ShadingLanguageX.

| Statement             | Example                                      |
|-----------------------|----------------------------------------------|
| Variable Declaration  | `float a = 0.714;`                           |
| Variable Assignment   | `a = 0.667;`                                 |
| Compound Assignment   | `a *= 10.0;`                                 |
| Function Declaration  | `float add_one(float a) { return a + 1.0; }` |
| For Loop              | `for (int i = 0:10) { a = add_one(a); }`     |
| Expression Statement  | `standard_surface(base_color=color3(a));`    |

# Identifiers

Identifiers are the names given to user-defined variables and functions so they can be accessed later in the program.
Identifiers can contain letters, numbers and the underscore character, but the first character cannot be a number.
They cannot be the same as a ShadingLanguageX reserved keyword (see below) or a MaterialX Standard Node.

### Examples

```
int i = 0;
int _i = i + 1;
vec3 __UP__ = vec3(0.0, 1.0, 0.0);
float n_angle = dotproduct(__UP__, normal());
float pi2 = 3.14 * 2.0;
```

# Reserved Keywords

The following identifiers have a special meaning in ShadingLanguageX and cannot be used for user-defined variables or functions.

`if` `else` `switch` `for` `return` `true` `false` `and` `or` `not` `void`

All data types and alias types are also reserved keywords.

### Notes

ShadingLanguageX is an evolving language. Keywords might be added in each update which might cause shaders to raise a compile
error which were previously working correctly. In general, try not to use identifiers that are popular keywords in other
languages (e.g., `const` `struct` `typeof`) or a term that is prominantly used in the MaterialX specification. 

# Whitespace

All whitespace is treated equally in ShaderLanguageX. A single space character is the same as 10 new line characters. For example:  
  
`float a = 1.0;`  
  
is equivalent to:
```
float
a
=
1.0
;
```
although we do not recommend the latter for readability reasons.

# Comments

Comments in ShandingLanguageX take the sole form of: `// this is a comment`.

# Operators

| Operation | MaterialX Node(s)   |
|-----------|---------------------|
| `a + b`   | `add`               |
| `a - b`   | `subtract`          |
| `a * b`   | `multiply`          |
| `a / b`   | `divide`            |
| `a % b`   | `modulo`            |
| `a ^ b`   | `power` or `xor`    |
| `a > b`   | `ifgreater`         |
| `a >= b`  | `ifgreatereq`       |
| `a < b`   | `ifgreatereq`       |
| `a <= b`  | `ifgreater`         |
| `a == b`  | `ifequal`           |
| `a != b`  | `ifequal`+`not`     |
| `a & b`   | `and`               |
| `a and b` | `and`               |
| `a \| b`  | `or`                |
| `a or b`  | `or`                |
| `-a`      | `subtract`          |
| `+a`      | -                   |
| `!a`      | `not`               |
| `not a`   | `not`               |
| `a[b]`    | `extract`           |
| `a.b`     | `extract`+`combine` |
| `(a)`     | -                   |

### Notes

* The `^` operator compiles to a `power` node when used with numeric types and to an `xor` node when used with booleans.
* The MaterialX arithmetic nodes specify that vectors/colors must be the first input if paired with a float, however this 
is not the case in ShadingLanguageX, a vector/color can be either the left or right value, for example, `2.0 * vec3()` 
is equivlant to `vec3() * 2.0`.

## Ternary Relational Operator

ShadingLanguageX supports the Ternary Relational Operator: `a < x < b`, which is equivalent to `a < x and x < b`.
This form can be used with any of the relational operators (i.e., `<` `<=` `>` `>=`).

## Swizzle Operator

Currently, the only expression that uses the period character `a.b` is the Swizzle Operator. The Swizzle Operator allows
users to access vector components using any of `x` `y` `z` `w` or color channels using `r` `g` `b` `a` after the period. 
For example, `vec3 b = a.yyz;` is equivalent to `vec3 b = vec3(a.y, a.y, a.z);`.
The characters `x` `y` `z` `w` can only be used to access components from a vector, it is a syntax error to use them with
a color type variable. The opposite is then true for `r` `g` `b` `a`. 
Swizzles can be made from any combination of valid characters, with a maximum number of 4 characters. However, a character cannot
be used that goes beyond the length of original vector, for example, `a.xyz` is an invalid swizzle for a variable of type 
`vec2` because it does not have a z component.
Finally, vector swizzles will always return a vector or `float` type variable, the specific type is dependant on the swizzle, for example 
`a.xy` return a `vec2`, while `a.zyzy` returns a `vec4`. Appropriately, color swizzles only return color or `float` type variables.

### Examples

`float alpha = image("alpha_mask.png").a;`  
`vec2 left_wall_uv = position().yz;`  
`color3 all_red = randomcolor().rrr;`

## Precendence 

| Order of Precendence (higher operations evaluate first) |
|---------------------------------------------------------|
| `(a)`                                                   |
| `a.b` `a[b]`                                            |
| `-a` `+a` `!a` `not a`                                  |
| `a ^ b`                                                 |
| `a * b` `a / b` `a % b`                                 |
| `a + b` `a - b`                                         |
| `a > b` `a >= b` `a < b` `a <= b`                       |
| `a == b` `a != b`                                       |
| `a & b` `a and b` `a \| b` `a or b`                     |

When two operators with equal precedence are used, the leftmost operator with evaluate first.  
As shown in the table above, precendence can be controlled using the Grouping Operator `(a)`. For example, in the expression
`a + b * c`, the `b * c` will evaluate first, however, in the expression `(a + b) * c`, the `a + b` will evaluate first.

# Variable Declarations

`type name = initial-value;`  
`type` can be any supported data type as listed earlier.  
`name` can be any valid identifier.  
`initial-value` can be any valid expression that evaluates to `type`.   

### Notes

* The `initial-value` is not optional as in most other languages.
* Variables cannot be re-declared. Declaring a variable that has already been declared in the current scope will result in a compile error. 

### Examples

`float a = 1.0;`  
`float b = a;`  
`bool is_positive = b > 0.0;`  
`int uv_channel = 3;`  
`vec2 uv = 1.0 - texcoord(uv_channel);`  
`string space = "world";`  
`surfaceshader surface = standard_surface();`

# Variable Assignment

`name = value;`  
`name` must be the name of an previously declared variable.  
`value` is any valid expression.

### Examples

`color4 albedo = color4();`  
`albedo = if (cond1) { image("butterfly1.png") };`  
`albedo = if (cond2) { image("butterfly2.png") };`  
`albedo = if (cond3) { image("butterfly3.png") };`

## Compound Assignment

| Assignment  | Expands to     |
|-------------|----------------|
| `a += b;`   | `a = a + b;`   |
| `a -= b;`   | `a = a - b;`   |
| `a *= b;`   | `a = a * b;`   |
| `a /= b;`   | `a = a / b;`   |
| `a %= b;`   | `a = a % b;`   |
| `a ^= b;`   | `a = a ^ b;`   |
| `a &= b;`   | `a = a & b;`   |
| `a \|= b;`  | `a = a \| b;`  |

# Constructors

`type(...)`  
`type` can be `bool` `int` `float` `vec2` `vec3` `vec4` `color3` `color4`.  

The constructor has the same name as the type itself and accepts zero or more arguments. 
The behaviour of the constructor changes depending on the number of arguments provided,
but will always return a variable of the corresponding type.

## Zero Arguments

In the case that no arguments are passed to the constructor a default value will be returned.

| Data Type | Default Value                |
|-----------|------------------------------|
| `bool`    | `false`                      |
| `int`     | `0`                          |
| `float`   | `0.0`                        |
| `vec2`    | `vec2(0.0, 0.0)`             |
| `vec3`    | `vec3(0.0, 0.0, 0.0)`        |
| `vec4`    | `vec4(0.0, 0.0, 0.0, 1.0)`   |
| `color3`  | `color3(0.0, 0.0, 0.0)`      |
| `color4`  | `color4(0.0, 0.0, 0.0, 1.0)` |

## One Argument

With a single argument, the constructor will convert the argument to the type of the constructor.
Currently, this simply compiles to the `convert` node. For information regarding supported conversions, 
see the MaterialX Standard Node document.

### Notes

ShadingLanguageX does not support implicit conversions. Explicit conversions can be achieved using constructors with a single argument.

### Examples

`float shadow = float(x > y);`  
`color3 white = color3(1.0);`  
`color3 i_debug = color3(viewdirection());`

## Two Or More Arguments

Two or more arguments has the following behaviour. It will take components from incoming arguments until all of its own
components have been filled and then discard the rest. If not enough components were provided, then the remaining will be `0.0`.

### Examples

`vec2 a = vec2(1.0, 2.0);`  
`vec3 b = vec3(a, 3.0); // will be vec3(1.0, 2.0, 3.0)`  
`vec4 c = vec4(4.0, a); // will be vec4(4.0, 1.0, 2.0, 0.0)`

# If Expressions

Unlike most languages, ShaderLanguageX does not support if statements, but instead uses if expressions. This is because if expressions
are a better match for how MaterialX handles conditionals. You can think of if expressions as similar to the C ternary operator.

`if (condition) { value_if_true } else { value_if_false }`  
`condition` must evaluate to a bool type.  
The if expression will evaluate to `value_if_true` if the condition is true, otherwise `value_if_false`. 

The syntax `if (condition) { value_if_true }` can be used during an assignment statement. In this case, if the condition
evaluates to false, the variable will retain its original value.

As mentioned earlier, ShadingLanguageX does not support implicit type conversions. As such, both sides of the if expression
are expected to evaluate to the same type. 

### Examples

`float a = if (x > y) { 0.05 } else { 0.07 };`  
`a = if (z > x) { 0.09 };` equivalent to `a = if (z > x) { 0.09 } else { a };`  

```
vec3 upaxis = if (target_platform == UNREAL) 
{ 
    vec3(0.0, 0.0, 1.0) 
} 
else 
{ 
    vec3(0.0, 1.0, 0.0) 
};
```

# Switch Expressions

ShaderLanguageX also does not support switch statements, but instead uses switch expressions, for the same reasons as if 
expressions above. They are similar to switch expressions found in the C# language.

`switch (which) { in1, in2, in3 }`  
`which` can evaluate to either an `int` or `float` type.  
The switch expression will evaluate to either `in1`, `in2`, `in3`, or a default value depending on the value of `which`.
See the `switch` node in the MaterialX Standard Node document for more information.

### Examples

```
color4 albedo = switch (wall_id)
{
    image("left_wall.png", texcoord=uv),
    image("right_wall.png", texcoord=uv),
    image("back_wall.png", texcoord=uv),
    image("ceiling.png", texcoord=uv),
    image("floor.png", texcoord=uv)
}
```

# For Loops

Unlike if and switch expressions, loops are compiled as statements in ShadingLanguageX, with the caveat that the number of
loop iterations must be known at compile time. 

```
for (type name = start-value:end-value)
{
    statement*
}
```
`type` can either be `int` or `float`.  
`name` can be any valid identifier.  
`start-value` is the value that the iteration value will start from.  
`end-value` is the value that the iteration value will stop at. It is included in the loop.  
For example, `0:3` will iterate through the values `0` `1` `2` `3`.

For loops can also be declared with an incremement value. Instead of increasing the iteration value by 
`1` each loop, it will be increased by the value of the specified increment instead. The syntax in this case looks like
this: `start-value:increment-value:end-value`. For example, `0:2:6` would result in the following sequence: `0` `2` `4` `6`.

### Examples

```
// render 10 randomly sized white circles
color3 c = color3();
for (int i = 0:9)
{
    vec2 center = vec2(randomfloat(seed=i), randomfloat(seed=i+10));
    c = if (distance(center, texcoord()) < randomfloat(max=0.1, seed=i+20)) { color3(1.0) };
}
standard_surface(base_color=c);
```

# User Functions

## Function Declaration

Users can declare there own functions in ShadingLanguageX using the following syntax:
```
type name(param1_type param1_name, param2_type param2_name...)
{
    statement*
    return value;
}
```
`type` can be any supported data type. It can also be `void` to indicate that function does not return a value.
In this case, the return statement should also be omitted.  
`name` can be any valid identifier.  
`paramN_type` can be any supported data type and `paramN_name` can be any valid identifier. Functions can declare any number of parameters.  
There is no concept of pointers or out parameters in ShadingLanguageX. Arguments are purely used to pass data into the function.

## Function Calls

The other half of user functions is then calling them.

`name(arg1, arg2...)`  
`name` is the name of function to be invoked.  
`argN` is N number of expressions whose data types exactly match those in the function signature.

### Examples

```
float mad(float m, float a, float b)
{
    return m * a + b;
}

float f = mad(1.0, 2.0, 3.0);
```
```
void main(color3 c, float intensity, vec3 n)
{
    surfaceshader surface = standard_surface();
    surface.base_color = c * intensity;
    surface.normal = n;
}

vec3 n = image("normals.png");
main(color3(3.0, 7.0, 5.0), 0.8, n);
```

### Notes

* Currently, ShadingLanguageX does not support function overloading, but it is in the list of proposals for language features.  
* All parameters must be fulfilled when calling the function, i.e., if a function declares two parameters, then two arguments of the correct type must be given when calling that function. It is not possible to provide default values to parameters like Python and other languages.
* Functions must be declared prior to being called.  
* Functions can be declared inside other functions, but will only be available to be called from within the enclosing function
and only after the enclosed function has been declared.
* Recursion is not possible in ShadingLanguageX. 

# Standard Library Call



# Node Constructors

Node constructors are a unique expression to ShadingLanguageX, but provide crucial functionality.

`{string, type: input1=value1, input2=value2...}`  
`string` can be any valid string value.    
`type` can be any supported data type.  
`inputN` can be any valid identifier.
`valueN` can be any valid expression.

Node constructors compile to the node specified by `string` and a type specified by `type`. Node inputs are specified by
the list of inputs that come after the colon `:`. It's important to note that, unlike the rest of ShadingLanguageX, node 
constructors do not perform any type checking. In fact, the data type of the inputs is determined by the values that are
passed to them.

Node constructors give developers the ability to define any node that they want, regardless of whether it is implemented
in ShadingLanguageX or not. For example, the `normalmap` node from the MaterialX Standard Node specification changed signature
in v1.39. However, many renderers are still using the v1.38 signature. Node constructors can be used to create node elements
with the old input signature to ensure compatability with as many renderers as possible. Node constructos can also be used to declare nodes that are not defined
in the MaterialX specification, such as renderer specific nodes.

### Examples

#### Normalmap compatability
```
vec3 nt = image("normals.png");
vec3 nm = {"normalmap", vec3: in=nt, space="tangent", scale=0.1};
```
Compiled .mtlx file:
```
...
<normalmap name="nm" type="vector3">
  <input name="in" type="vector3" nodename="nt" />
  <input name="space" type="string" value="tangent" />
  <input name="scale" type="float" value="0.1" />
</normalmap>
...
```

#### Renderer-specific nodes
```
// Houdini bias node
float bias = {"hmtlxbias", float: in=0.0, bias=0.5};
```