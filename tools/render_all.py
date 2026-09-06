#!/usr/bin/env python3
"""Run the heavy render stages in sequence (meant to run in background)."""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("LD_LIBRARY_PATH", os.path.expanduser("~/.wk_xstubs"))

from world_kit import pipeline

ORDER = ["assets", "reuse", "showcase", "stills", "pano", "walk", "catalog"]

for stage in ORDER:
    t0 = time.time()
    print(f"[render_all] START {stage}", flush=True)
    try:
        pipeline.run(stage)
        print(f"[render_all] DONE {stage} in {time.time()-t0:.0f}s", flush=True)
    except Exception as e:  # keep going, log it
        print(f"[render_all] FAIL {stage}: {e}", flush=True)
print("[render_all] ALL COMPLETE", flush=True)
