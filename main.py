#!/usr/bin/env python3
"""Entry program: copy the bundled entry.png to the output directory.

Runs offline with the standard library only. The output directory comes
from the MAKEFUN_OUTPUT_DIR environment variable (default /output).
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
