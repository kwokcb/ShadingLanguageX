import os
import subprocess
import sys
import time
from threading import Thread

# Re-compiles and updates houdini references to MaterialX files.

# path to mxslc executable
MXSLC_PATH = r"your\path\to\mxslc.exe"

# path to .mxsl file or directory containing .mxsl files
SHADER_PATH = r"your\path\to\shaders"


def compile_and_enable_references():
    # execute mxslc and print output
    result = subprocess.run([MXSLC_PATH, SHADER_PATH], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout[:-1])
    if result.stderr:
        print(result.stderr)

    # re-enable reference nodes
    for n in ref_nodes:
        n.parm("enable1").set(True)

if not os.path.exists(MXSLC_PATH):
    print(f"Invalid mxslc.exe path: {MXSLC_PATH}")
    sys.exit()

# get all reference nodes
ref_nodes = [n for n in hou.node("/stage").allSubChildren() if "reference" in n.type().name()]

# disable reference nodes
for n in ref_nodes:
    n.parm("enable1").set(False)

# compile and re-enable reference nodes on a separate thread
t = Thread(target=compile_and_enable_references)
t.start()
