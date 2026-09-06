#!/bin/bash
export LD_LIBRARY_PATH=/home/user/World_Set/work/stublibs
cd /home/user/World_Set
step () { echo "=== START $1 $(date +%T)"; python3 tools/$1 2>&1 | grep -vi "cuew\|use_nodes" | tail -${2:-6}; echo "=== END $1 rc=${PIPESTATUS[0]} $(date +%T)"; }
step export_glb.py 4
step render_thumbs.py 3
step make_materials.py 4
step render_stills.py 10
step render_pano.py 3
step render_walk.py 3
step make_video.py 6
echo "=== CHAIN COMPLETE $(date +%T)"
