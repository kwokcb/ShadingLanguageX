from pathlib import Path


class SourceFile:
    def __init__(self, path: Path):
        self.__path = path
        with open(path, "r") as f:
            self.__source = f.read()

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def source(self) -> str:
        return self.__source

    @source.setter
    def source(self, source: str) -> None:
        self.__source = source
