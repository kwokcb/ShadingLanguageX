from .Argument import Argument
from .Keyword import *
from .Parameter import ParameterList, ParameterTuple


class StandardLibrary(StrEnum):
    IMAGE = auto()
    RANDOMFLOAT = auto()
    NOISE2D = auto()
    POSITION = auto()
    NORMAL = auto()
    TANGENT = auto()
    VIEWDIRECTION = auto()
    TEXCOORD = auto()
    TIME = auto()
    FRACT = auto()
    ABSVAL = auto()
    FLOOR = auto()
    CEIL = auto()
    ROUND = auto()
    SIN = auto()
    COS = auto()
    EXP = auto()
    CLAMP = auto()
    MIN = auto()
    MAX = auto()
    NORMALIZE = auto()
    MAGNITUDE = auto()
    DISTANCE = auto()
    DOTPRODUCT = auto()
    CROSSPRODUCT = auto()
    NORMALMAP = auto()
    MIX = auto()
    STANDARD_SURFACE = auto()

    def return_type(self, assignment_data_type: DataType, arg0_data_type: DataType) -> DataType:
        if self in self.IMAGE:
            return assignment_data_type or COLOR4

        if self in [self.POSITION, self.NORMAL, self.TANGENT, self.VIEWDIRECTION, self.CROSSPRODUCT, self.NORMALMAP]:
            return VECTOR3
    
        if self in self.TEXCOORD:
            return VECTOR2
    
        if self in [self.RANDOMFLOAT, self.TIME, self.MAGNITUDE, self.DISTANCE, self.DOTPRODUCT]:
            return FLOAT
    
        if self in [self.FRACT, self.ABSVAL, self.FLOOR, self.CEIL, self.ROUND, self.SIN, self.COS, self.EXP,
                    self.CLAMP, self.MIN, self.MAX, self.NORMALIZE, self.NOISE2D, self.MIX]:
            return arg0_data_type
    
        if self in self.STANDARD_SURFACE:
            return SURFACESHADER
    
        raise AssertionError(f"No return type defined for '{self}'.")

    def parameters(self, args: list[Argument] = None) -> ParameterList:
        # at the moment there is only one overload, if more are added, let's handle it a more elegant way
        if self is self.IMAGE and args is not None and len(args) >= 2 and args[1].data_type == VECTOR2:
            return ParameterList([("file", FILENAME), ("texcoord", VECTOR2), ("filtertype", STRING), ("default", FLOAT_TYPES), ("layer", STRING), ("uaddressmode", STRING), ("vaddressmode", STRING)])

        params: dict[str, list[ParameterTuple]] = {
            self.IMAGE: [("file", FILENAME), ("layer", STRING), ("default", FLOAT_TYPES), ("texcoord", VECTOR2), ("uaddressmode", STRING), ("vaddressmode", STRING), ("filtertype", STRING)],
            self.RANDOMFLOAT: [("in", [FLOAT, INTEGER]), ("min", FLOAT), ("max", FLOAT), ("seed", INTEGER)],
            self.NOISE2D: [("amplitude", [FLOAT, *VECTOR_TYPES]), ("pivot", FLOAT), ("period", [FLOAT, *VECTOR_TYPES]), ("texcoord", VECTOR2)],
            self.POSITION: [("space", STRING)],
            self.NORMAL: [("space", STRING)],
            self.TANGENT: [("space", STRING)],
            self.VIEWDIRECTION: [("space", STRING)],
            self.TEXCOORD: [("index", INTEGER)],
            self.TIME: [],
            self.FRACT: [("in", [FLOAT, *VECTOR_TYPES])],
            self.ABSVAL: [("in", FLOAT_TYPES)],
            self.FLOOR: [("in", FLOAT_TYPES)],
            self.CEIL: [("in", FLOAT_TYPES)],
            self.ROUND: [("in", FLOAT_TYPES)],
            self.SIN: [("in", [FLOAT, *VECTOR_TYPES])],
            self.COS: [("in", [FLOAT, *VECTOR_TYPES])],
            self.EXP: [("in", [FLOAT, *VECTOR_TYPES])],
            self.CLAMP: [("in", FLOAT_TYPES), ("low", FLOAT_TYPES), ("high", FLOAT_TYPES)],
            self.MIN: [(f"in{i+1}", FLOAT_TYPES) for i in range(10)],
            self.MAX: [(f"in{i+1}", FLOAT_TYPES) for i in range(10)],
            self.NORMALIZE: [("in", VECTOR_TYPES)],
            self.MAGNITUDE: [("in", VECTOR_TYPES)],
            self.DISTANCE: [("in1", VECTOR_TYPES), ("in2", VECTOR_TYPES)],
            self.DOTPRODUCT: [("in1", VECTOR_TYPES), ("in2", VECTOR_TYPES)],
            self.CROSSPRODUCT: [("in1", VECTOR3), ("in2", VECTOR3)],
            self.NORMALMAP: [("in", VECTOR3), ("space", STRING), ("scale", [FLOAT, VECTOR2]), ("normal", VECTOR3), ("tangent", VECTOR3), ("bitangent", VECTOR3)],
            self.MIX: [("bg", FLOAT_TYPES), ("fg", FLOAT_TYPES), ("mix", FLOAT_TYPES)],
            self.STANDARD_SURFACE: [("base_color", COLOR3), ("metalness", FLOAT), ("specular_roughness", FLOAT), ("normal", VECTOR3)],
        }

        if self in params:
            return ParameterList(params[self])

        raise AssertionError(f"No parameters defined for '{self}'.")

    def parameter_type(self, param_name: str) -> DataType:
        return self.parameters()[param_name].data_types[0]
