import sys
from pathlib import Path

from . import mtlx, state
from .compile import compile
from .parse import parse
from .post_process import post_process
from .pre_process import pre_process
from .scan import scan


def compile_file(mxsl_filepath: str | Path) -> None:
    mxsl_filepath = Path(mxsl_filepath)

    with open(mxsl_filepath, "r") as file:
        code = file.read()

    xml = compile_string(code)

    mtlx_filepath = mxsl_filepath.with_suffix(".mtlx")
    with open(mtlx_filepath, "w") as file:
        file.write(xml)

    print(f"{mxsl_filepath.name} compiled successfully.")


def compile_string(mxsl_code: str) -> str:
    mtlx.clear()
    state.clear()

    mxsl_code = pre_process(mxsl_code, defines=[])
    tokens = scan(mxsl_code)
    statements = parse(tokens)
    compile(statements)
    post_process()

    return mtlx.get_xml()


if __name__ == "__main__":
    compile_file(sys.argv[1])
