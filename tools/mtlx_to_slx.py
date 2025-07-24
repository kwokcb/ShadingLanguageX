import sys
import argparse
from pathlib import Path

try:
    # Import the Decompiler class directly from the module where it's defined
    from mxslc.Decompiler.decompile import Decompiler
except ImportError as e:
    print(f"Error: Could not import Decompiler. Error: {e}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Convert MaterialX files to SLX format.")
    parser.add_argument(dest='input_file', help="Path to the input MaterialX file (.mtlx)")
    parser.add_argument("-o", "--output_file", dest="output_file", default="", type=str, help="Path to the output SLX file (.slx)")
    
    args = parser.parse_args()
    input_file = Path(args.input_file)
    if not input_file.exists():
        print(f"Input file does not exist: {input_file}")
        sys.exit(1)
    
    decompiler = Decompiler(input_file)
    
    # Decompile the MaterialX file
    try:
        mxsl_output = decompiler.decompile()
    except Exception as e:
        print(f"Error during decompilation: {e}")
        sys.exit(1)
    
    output_file = args.output_file
    if len(output_file) == 0:
        print(mxsl_output)
    else:
        output_file = Path(output_file)
        with open(output_file, "w") as f:
            f.write(mxsl_output)
        print(f"Output written to: {output_file}")
    
if __name__ == "__main__":
    main()
