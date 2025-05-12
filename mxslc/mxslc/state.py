from __future__ import annotations

from . import mtlx
from .CompileError import CompileError
from .Statements import FunctionDeclaration, ForLoop
from .Token import Token
from .scan import as_token


class State:
    def __init__(self, namespace: str, global_: State = None, parent: State = None):
        self.__namespace = namespace
        self.__global = global_ or self
        self.__parent = parent
        self.__nodes: dict[str, mtlx.Node] = {}
        self.__functions: dict[str, FunctionDeclaration] = {}

    @property
    def is_global(self) -> bool:
        return self == self.__global

    @property
    def global_(self) -> State:
        return self.__global

    @property
    def parent(self) -> State:
        return self.__parent

    def add_node(self, identifier: Token, node: mtlx.Node) -> None:
        name = identifier.lexeme
        if name in self.__nodes:
            raise CompileError(f"Variable name '{name}' already exists.", identifier)
        assert node not in self.__nodes.values()
        self.__nodes[name] = node
        node.name = self.get_full_name(name)

    def get_node(self, identifier: Token) -> mtlx.Node:
        name = identifier.lexeme
        if name in self.__nodes:
            return self.__nodes[name]
        if self.__namespace == ForLoop.NAMESPACE:
            try:
                return self.__parent.get_node(identifier)
            except CompileError:
                ...
        if name in self.__global.__nodes:
            return self.__global.__nodes[name]
        raise CompileError(f"Variable name '{name}' does not exist.", identifier)

    def set_node(self, identifier: Token, node: mtlx.Node) -> None:
        name = identifier.lexeme
        assert node not in self.__nodes.values()
        if name in self.__nodes:
            self.__nodes[name] = node
            node.name = self.get_full_name(name)
            return
        if self.__namespace == ForLoop.NAMESPACE:
            try:
                self.__parent.set_node(identifier, node)
                return
            except CompileError:
                ...
        # If I wanted to let developers set global variables I would do it here
        raise CompileError(f"Variable name '{name}' does not exist.", identifier)

    def clear(self) -> None:
        self.__nodes.clear()
        self.__functions.clear()

    def get_full_name(self, name: str) -> str:
        return f"{self.__namespace}__{name}"

    def add_function(self, func: FunctionDeclaration) -> None:
        if func.name in self.__functions:
            raise CompileError(f"Function name '{func.name}' already exists.", func.identifier)
        assert func not in self.__functions.values()
        self.__functions[func.name] = func

    def get_function(self, identifier: Token) -> FunctionDeclaration:
        name = identifier.lexeme
        if name in self.__functions:
            return self.__functions[name]
        if name in self.__global.__functions:
            return self.__global.__functions[name]
        raise CompileError(f"Function name '{name}' does not exist.", identifier)

    def __str__(self) -> str:
        output = ""
        output += "self: " + self.__namespace + "\n"
        output += "parent: " + (self.__parent.__namespace if self.__parent else "None") + "\n"
        output += "global: " + self.__global.__namespace + "\n"
        output += "----------------" + "\n"
        for name, node in self.__nodes.items():
            output += f"{name}: {node.data_type} {node.name}\n"
        return output


_state = State("global")


def add_node(identifier: Token, node: mtlx.Node) -> None:
    _state.add_node(identifier, node)


def get_node(identifier: str | Token) -> mtlx.Node:
    return _state.get_node(as_token(identifier))


def set_node(identifier: str | Token, node: mtlx.Node) -> None:
    _state.set_node(as_token(identifier), node)


def is_node(identifier: str) -> bool:
    try:
        get_node(identifier)
        return True
    except CompileError:
        return False


def clear() -> None:
    global _state
    while not _state.is_global:
        _state = _state.__parent
    _state.clear()


def add_function(func: FunctionDeclaration) -> None:
    _state.add_function(func)


def get_function(identifier: str | Token) -> FunctionDeclaration:
    return _state.get_function(as_token(identifier))


def is_function(identifier: str) -> bool:
    try:
        get_function(identifier)
        return True
    except CompileError:
        return False


def enter_scope(namespace: str) -> None:
    global _state
    _state = State(namespace, _state.global_, _state)


def exit_scope() -> None:
    global _state
    _state = _state.parent


def print_scope_info() -> None:
    global _state
    print(_state)
