import re


def pre_process(source: str, defines: list[str]):
    source = _remove_comments(source)
    source = _remove_undefined_blocks(source, defines)
    source = _add_call_to_main(source)
    return source


def _remove_comments(source: str) -> str:
    return re.sub(r"//.*", "", source)


# TODO preprocessing the define blocks will change line numbers in CompileErrors, maybe process it as tokens.
def _remove_undefined_blocks(source: str, defines: list[str]) -> str:
    ifs = re.findall(r"#IF\s+(\w+)", source)
    undefined_ifs = set(ifs) - set(defines)
    for undefined_if in undefined_ifs:
        source = re.sub(rf"\s*#IF\s+{undefined_if}\s+(.|\n|\r)*?#ENDIF", "", source)
    source = re.sub(r"\s*#IF\s+(\w+)", "", source)
    source = re.sub(r"\s*#ENDIF", "", source)
    return source


# TODO make this a lot more robust
def _add_call_to_main(source: str) -> str:
    if "surfaceshader main()" in source:
        return source + "\n\nsurfaceshader __surface__ = main();\n"
    return source
