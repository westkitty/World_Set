#!/usr/bin/env bash
# Bootstrap the headless Blender (bpy) toolchain used by the WORLD KIT pipeline.
#
# The pipeline runs on the `bpy` PyPI wheel (Blender 4.5 LTS as a Python module).
# On a minimal Linux box the wheel links against a few X11/GL libraries that may
# be absent; we build tiny no-op stubs for them (headless Cycles/glTF never call
# into a display).  This script is idempotent.
set -euo pipefail

VENV="${VENV:-$HOME/.venv}"
STUBS="${STUBS:-$HOME/.wk_xstubs}"

if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install --upgrade pip >/dev/null
"$VENV/bin/pip" install "bpy==4.5.13" pillow >/dev/null

# --- stub shared libraries so the bundled Blender can load headless --------
if [ ! -f "$STUBS/libXfixes.so.3" ]; then
  mkdir -p "$STUBS"
  cat > "$STUBS/stubs.c" <<'EOF'
#include <stddef.h>
int wk_marker = 0;
void XFixesHideCursor(void){} void XFixesShowCursor(void){}
void *XCloseDevice(void){return 0;} void *XFreeDeviceList(void){return 0;}
void *XFreeDeviceState(void){return 0;} void *XGetExtensionVersion(void){return 0;}
void *XListInputDevices(void){return 0;} void *XOpenDevice(void){return 0;}
void *XQueryDeviceState(void){return 0;} int XSelectExtensionEvent(void){return 0;}
void *_XiGetDevicePresenceNotifyEvent(void){return 0;}
void *glFinish(void){return 0;} void *glXSwapBuffers(void){return 0;}
static void *wk_noop(void){return 0;}
void *glXGetProcAddress(void){return (void*)wk_noop;}
void *glXGetProcAddressARB(void){return (void*)wk_noop;}
EOF
  gcc -shared -fPIC -o "$STUBS/libXfixes.so.3" -Wl,-soname,libXfixes.so.3 "$STUBS/stubs.c"
  gcc -shared -fPIC -o "$STUBS/libXi.so.6"     -Wl,-soname,libXi.so.6     "$STUBS/stubs.c"
  for n in libXrender.so.1 libSM.so.6 libICE.so.6 libGL.so.1; do
    gcc -shared -fPIC -o "$STUBS/$n" -Wl,-soname,$n "$STUBS/stubs.c"
  done
fi

echo "WORLD KIT toolchain ready:"
echo "  venv : $VENV"
echo "  stubs: $STUBS"
echo "Run with:  LD_LIBRARY_PATH=$STUBS $VENV/bin/python tools/wk.py --stage all"
