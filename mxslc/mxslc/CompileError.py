class CompileError(Exception):
    def __init__(self, line: int, message: str):
        super().__init__(f"Line {line}: {message}")
