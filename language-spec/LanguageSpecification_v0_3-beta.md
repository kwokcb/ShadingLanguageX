# Overview

ShadingLanguageX is a high level shading language that can be used to write shaders that can be compiled into MaterialX (.mtlx) files.
The primary use case is to provide a method of creating MaterialX materials without the use a node editor or the MaterialX C++ or Python APIs.
Node editors are useful for creating simple material networks, but become combersome for larger networks. 
At the same time, the MaterialX API is verbose, making it difficult to quickly iterate when writing a shader.
ShadingLanguageX is a simple, yet powerful language for writing complex MaterialX shaders.

At the end of the day, ShadingLanguageX is based on the MaterialX specification and we've striven for equavilency as much
as possible. As such, if anything is omitted from this document, you can assume that the behaviour is the same as what is
described in the official MaterialX specification. For example, we don't specify in this document what is the return 
type of a `float` multiplied by a `vector3`, as it is already described in the MaterialX Standard Node [document](https://github.com/AcademySoftwareFoundation/MaterialX/blob/main/documents/Specification/MaterialX.StandardNodes.md). 
This allows this document to be as concise as possible as well as reducing the chance of needing to update it based on changes
to the official MaterialX documentation.

# Data Types
Data types match the ones found in the MaterialX [specification](https://github.com/AcademySoftwareFoundation/MaterialX/blob/main/documents/Specification/MaterialX.Specification.md#materialx-data-types), with the expection of arrays, matrices, volumeshader and lightshader.  
  
### Supported Data Types
* `boolean`
* `integer`
* `float`
* `vector2`
* `vector3`
* `vector4`
* `color3`
* `color4`
* `string`
* `filename`
* `surfaceshader`
* `displacementshader`

### Type Aliases
* `boolean` ➔ `bool`
* `integer` ➔ `int`
* `vector2` ➔ `vec2`
* `vector3` ➔ `vec3`
* `vector4` ➔ `vec4`

# Operators

| Operation | Compiles To         |
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

## Notes

The `^` operator compiles to a `power` node when used with float types and to an `xor` node when used with booleans.

The MaterialX arithmetic nodes specify that vectors/colors must be the first input if paired with a float, however this 
is not the case in ShadingLanguageX, a vector/color can be either the left or right value, for example, `2.0 * my_vec3` 
is equivlant to `my_vec3 * 2.0`.

## Ternary Relational Operator

ShadingLanguageX supports the Ternary Relational Operator: `a < x < b` is equivalent to `a < x and x < b`.
This form can be used with any of the relational operators (i.e., `<`, `<=`, `>`, `>=`).

## Swizzle Operator

Currently, the only expression that uses the period character `a.b` is the Swizzle Operator. The Swizzle Operator allows
users to access vector components using any of `x`, `y`, `z`, `w` or color channels using `r`, `g`, `b`, `a` after the period. 
For example, `vec3 b = a.yyz` is equivalent to `vec3 b = vec3(a.y, a.y, a.z)`.
The characters `x`, `y`, `z`, `w` can only be used to access components from a vector, it is a syntax error to use them with
a color type variable. The opposite is then true to `r`, `g`, `b`, `a`. 
Swizzles can be made from any combination of valid characters, with a maximum number of 4 characters. However, a character cannot
be used that goes beyond the length of original vector, for example, `a.xyz` is an invalid swizzle for a variable of type 
`vector2` because it does not have a z component.
Finally, vector swizzles will always return a vector or `float` type variable, the specific type is dependant on the swizzle, for example 
`a.xy` return a `vector2`, while `a.zyzy` returns a `vector4`. Appropriately, color swizzles only return color or `float` type variables.

#### Examples

`float alpha = image("alpha_mask.png").a;`  
`vec2 left_wall_uv = position().yz;`  
`color3 all_red = randomcolor().rrr;`

## Precendence 

| Precendence (higher operations evaluate first) |
|------------------------------------------------|
| `(a)`                                          |
| `a.b` `a[b]`                                   |
| `-a` `+a` `!a` `not a`                         |
| `a ^ b`                                        |
| `a * b` `a / b` `a % b`                        |
| `a + b` `a - b`                                |
| `a > b` `a >= b` `a < b` `a <= b`              |
| `a == b` `a != b`                              |
| `a & b` `a and b` `a \| b` `a or b`            |

When two operators are used with equal precedence, the leftmost operator with evaluate first.  
As shown in the table above, precendence can be controlled using the Grouping Operator `(a)`. For example, in the expression
`a + b * c`, the `b * c` will evaluate first, however, in this expression `(a + b) * c`, the `a + b` will evaluate first.
