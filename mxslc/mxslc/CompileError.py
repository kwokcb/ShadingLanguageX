from pathlib import Path


class CompileError(Exception):
    def __init__(self, line: int, message: str, filepath: Path = None):
        if filepath is None:
            super().__init__(f"Line {line}: {message}")
        else:
            super().__init__(f"{filepath.absolute()}, line {line}: {message}")
