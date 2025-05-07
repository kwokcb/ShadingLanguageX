from pathlib import Path
from typing import Sequence

from . import mtlx, state
from .Argument import Argument
from .CompileError import CompileError
from .Expressions import ConstantExpression
from .Preprocess import macros
from .Preprocess.process import process as preprocess
from .Statements import Statement
from .parse import parse
from .post_process import post_process
from .scan import scan


def compile_file(mxsl_path: str | Path,
                 mtlx_path: str | Path = None,
                 *,
                 main_function: str = None,
                 main_args: Sequence[mtlx.Constant] = None,
                 add_include_dirs: Sequence[Path] = None) -> None:
    mxsl_filepaths = _handle_mxsl_path(mxsl_path)

    for mxsl_filepath in mxsl_filepaths:
        mtlx_filepath = _handle_mtlx_path(mtlx_path, mxsl_filepath)

        macros.clear()
        mtlx.clear()
        state.clear()

        include_dirs = (add_include_dirs or []) + [mxsl_filepath.parent, Path(".")]

        tokens = scan(mxsl_filepath)
        processed_tokens = preprocess(tokens, include_dirs)
        statements = parse(processed_tokens)
        _compile(statements)
        _call_main(mxsl_filepath, main_function, main_args or [])
        post_process()

        with open(mtlx_filepath, "w") as file:
            file.write(mtlx.get_xml())

        print(f"{mxsl_filepath.name} compiled successfully.")


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
    mtlx_path.parent.mkdir(parents=True, exist_ok=True)
    return mtlx_path


def _compile(statements: list[Statement]) -> None:
    for statement in statements:
        statement.execute()


def _call_main(file: Path, name: str | None, args: Sequence[mtlx.Constant]) -> None:
    try:
        main = state.get_function(name or "main")
    except CompileError as e:
        if name is not None:
            raise e
    else:
        if name is not None or main.file == file:
            main.invoke(_to_arg_list(args))

def _to_arg_list(args: Sequence[mtlx.Constant]) -> list[Argument]:
    return [Argument(ConstantExpression(a)) for a in args]
