#!/usr/bin/env python3
"""WORLD KIT pipeline CLI.

Usage:
    python tools/wk.py --stage all        # textures+assets+reuse+showcase+catalog
    python tools/wk.py --stage assets     # build kit, validate, export GLB, docs
    python tools/wk.py --stage stills     # render the 6 environment stills
    python tools/wk.py --stage pano       # render the 360 panorama
    python tools/wk.py --stage walk       # render the walkthrough video

Requires the bpy toolchain (see tools/bootstrap_env.sh).
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("LD_LIBRARY_PATH", os.path.expanduser("~/.wk_xstubs"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all",
                    choices=["all", "textures", "assets", "reuse", "showcase",
                             "stills", "pano", "walk", "catalog"])
    args = ap.parse_args()

    from world_kit import pipeline
    result = pipeline.run(args.stage)
    if result:
        report = result[0]
        for line in report:
            print(" -", line)
    print(f"[wk] stage '{args.stage}' complete")


if __name__ == "__main__":
    main()
