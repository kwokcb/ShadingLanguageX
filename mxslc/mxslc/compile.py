from pathlib import Path

from . import mtlx, state
from .Statements import Statement
from .parse import parse
from .post_process import post_process
from .pre_process import pre_process
from .scan import scan


def compile_string(mxsl_code: str) -> str:
    mtlx.clear()
    state.clear()

    mxsl_code = pre_process(mxsl_code, defines=[])
    tokens = scan(mxsl_code)
    statements = parse(tokens)
    _compile(statements)
    post_process()

    return mtlx.get_xml()


def compile_file(mxsl_path: str | Path, mtlx_path: str | Path = None) -> None:
    mxsl_files = _handle_mxsl_path(mxsl_path)

    for mxsl_file in mxsl_files:
        mtlx_file = _handle_mtlx_path(mtlx_path, mxsl_file)

        with open(mxsl_file, "r") as file:
            mxsl_code = file.read()

        mtlx_xml = compile_string(mxsl_code)

        with open(mtlx_file, "w") as file:
            file.write(mtlx_xml)

        print(f"{mxsl_file.name} compiled successfully.")


def _handle_mxsl_path(mxsl_path: str | Path) -> list[Path]:
    if mxsl_path is None:
        raise TypeError("Path to .mxsl file was empty.")
    if not isinstance(mxsl_path, str | Path):
        raise TypeError(f"Path to .mxsl file was an invalid type: '{type(mxsl_path)}'.")
    mxsl_path = Path(mxsl_path)
    if not mxsl_path.exists():
        raise FileNotFoundError(f"No such file or directory: '{mxsl_path}'.")
    if mxsl_path.is_file():
        return [mxsl_path]
    if mxsl_path.is_dir():
        return list(mxsl_path.glob("*.mxsl"))
    raise ValueError("Bad mxsl_path.")


def _handle_mtlx_path(mtlx_path: str | Path | None, mxsl_file: Path) -> Path:
    if mtlx_path is None:
        return mxsl_file.with_suffix(".mtlx")
    if not isinstance(mtlx_path, str | Path):
        raise TypeError(f"Path to .mtlx file was an invalid type: '{type(mtlx_path)}'.")
    mtlx_path = Path(mtlx_path)
    if mtlx_path.is_file():
        return mtlx_path
    if mtlx_path.is_dir():
        return mtlx_path / (mxsl_file.stem + ".mtlx")
    if mtlx_path.suffix != ".mtlx":
        mtlx_path /= (mxsl_file.stem + ".mtlx")
    mtlx_path.mkdir(parents=True, exist_ok=True)
    return mtlx_path


def _compile(statements: list[Statement]) -> str:
    for statement in statements:
        statement.execute()
    return mtlx.get_xml()
