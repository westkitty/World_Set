#!/usr/bin/env bash
# Run a WORLD KIT python step with the headless-Blender runtime in place.
#   tools/wk.sh tools/build_library.py
set -e
if [ ! -f "$HOME/stublibs/libGL.so.1" ]; then python3 "$(dirname "$0")/setup_env.py" >/dev/null; fi
export LD_LIBRARY_PATH="$HOME/stublibs:$LD_LIBRARY_PATH"
exec python3 "$@"
