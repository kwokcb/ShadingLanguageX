import re
from pathlib import Path

from .CompileError import CompileError
from .SourceFile import SourceFile


def pre_process(path: Path, other_include_dirs: list[Path], defines: list[str]) -> list[SourceFile]:
    processor = PreProcessor(path, other_include_dirs, defines, is_include=False)
    return processor.processed_files


class PreProcessor:
    MAIN_DEFINE = "__MAIN__"
    INCLUDE_DEFINE = "__INCLUDE__"

    def __init__(self, path: Path, other_include_dirs: list[Path], defines: list[str], is_include=False):
        self.__file = SourceFile(path)
        self.__other_include_dirs = other_include_dirs
        self.__include_dirs = other_include_dirs + [path.parent.absolute(), Path(".").absolute()]
        self.__defines = defines + [self.INCLUDE_DEFINE if is_include else self.MAIN_DEFINE]
        self.__included_files: list[SourceFile] = []

        self.__process_file()

    @property
    def processed_files(self) -> list[SourceFile]:
        return self.__included_files + [self.__file]

    @property
    def __source(self) -> str:
        return self.__file.source

    @__source.setter
    def __source(self, source: str) -> None:
        self.__file.source = source

    def __process_file(self) -> None:
        self.__remove_comments()
        self.__remove_undefined_blocks()
        if self.MAIN_DEFINE in self.__defines:
            self.__add_call_to_main()
        include_paths = self.__get_include_files()
        for include_path in include_paths:
            include_processor = PreProcessor(include_path, self.__other_include_dirs, self.__defines, is_include=True)
            self.__included_files.extend(include_processor.processed_files)
        self.__remove_include_directives()

    def __remove_comments(self) -> None:
        self.__source = re.sub(r"//.*", "", self.__source)

    def __remove_include_directives(self) -> None:
        self.__source = re.sub(r'#include\s*"([^"]+)"', "", self.__source)

    # TODO preprocessing the define blocks will change line numbers in CompileErrors
    def __remove_undefined_blocks(self) -> None:
        ifs = re.findall(r"#IF\s+(\w+)", self.__source)
        undefined_ifs = set(ifs) - set(self.__defines)
        for undefined_if in undefined_ifs:
            self.__source = re.sub(rf"\s*#IF\s+{undefined_if}\s+(.|\n|\r)*?#ENDIF", "", self.__source)
        self.__source = re.sub(r"\s*#IF\s+(\w+)", "", self.__source)
        self.__source = re.sub(r"\s*#ENDIF", "", self.__source)

    # TODO make this a lot more robust
    def __add_call_to_main(self) -> None:
        if "surfaceshader main()" in self.__source:
            self.__source += "\n\nsurfaceshader __surface__ = main();\n"

    def __get_include_files(self) -> list[Path]:
        filepaths: list[Path] = []
        for i, line in enumerate(self.__source.splitlines()):
            match = re.search(r'#include\s*"([^"]+)"', line)
            if match is None:
                continue
            path = self.__get_path(match.group(1))
            if path is None:
                raise CompileError(i, f"Include file not found: '{match.group(1)}'.", filepath=self.__file.path)
            if path.is_file():
                filepaths.append(path)
            if path.is_dir():
                for filepath in path.glob("*.mxsl"):
                    filepaths.append(filepath)

        return filepaths

    def __get_path(self, path: str) -> Path | None:
        path = Path(path)
        for include_dir in self.__include_dirs:
            if (include_dir / path).exists():
                return include_dir / path
        return None
