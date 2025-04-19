from argparse import ArgumentParser
from pathlib import Path

from mxslc import compile_file

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("mxsl_path", help="Input path to mxsl file or containing folder", type=Path)
    parser.add_argument("mtlx_path", nargs="?", help="Output path to generated mtlx file or containing folder", type=Path)
    args = parser.parse_args()

    try:
        compile_file(args.mxsl_path, args.mtlx_path)
    except Exception as e:
        print(e)
