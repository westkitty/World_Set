#!/bin/bash
export LD_LIBRARY_PATH=$HOME/stublibs
cd /home/user/World_Set
step () { echo "=== START $1 $(date +%T)"; python3 tools/$1 > work/log_${1%.py}.txt 2>&1; echo "=== END $1 rc=$? $(date +%T)"; }
STILL_W=1920 STILL_SPP=96 step render_stills.py
PANO_W=3072 PANO_SPP=56 step render_pano.py
rm -f work/frames/*.png
WALK_N=168 WALK_W=1024 WALK_SPP=16 step render_walk.py
FPS=12 step make_video.py
echo "=== CHAIN COMPLETE $(date +%T)"
