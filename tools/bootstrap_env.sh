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
if [ ! -f "$STUBS/libXfixes.so.3" ] || [ ! -f "$STUBS/libxkbcommon.so.0" ]; then
  mkdir -p "$STUBS"
  cat > "$STUBS/stubs.c" <<'EOF'
#include <stddef.h>
int wk_marker = 0;
static void *wk_dummy = &wk_marker;
void XFixesHideCursor(void){} void XFixesShowCursor(void){}
void *XCloseDevice(void){return 0;} void *XFreeDeviceList(void){return 0;}
void *XFreeDeviceState(void){return 0;} void *XGetExtensionVersion(void){return 0;}
void *XListInputDevices(void){return 0;} void *XOpenDevice(void){return 0;}
void *XQueryDeviceState(void){return 0;} int XSelectExtensionEvent(void){return 0;}
void *_XiGetDevicePresenceNotifyEvent(void){return 0;}
/* GL / GLX - never invoked by headless Cycles, only needed by the loader */
void glFinish(void){}
void glXSwapBuffers(void){}
void *glXGetProcAddress(void){return 0;}
void *glXGetProcAddressARB(void){return 0;}
void *glXChooseFBConfig(void){return 0;}
void *glXCreateContext(void){return wk_dummy;}
void *glXCreateNewContext(void){return wk_dummy;}
void *glXCreateWindow(void){return wk_dummy;}
void glXDestroyContext(void){}
void *glXGetCurrentContext(void){return wk_dummy;}
void *glXGetCurrentDisplay(void){return wk_dummy;}
void *glXGetCurrentDrawable(void){return wk_dummy;}
void *glXGetVisualFromFBConfig(void){return 0;}
int glXMakeContextCurrent(void){return 1;}
int glXMakeCurrent(void){return 1;}
int glXQueryContext(void){return 0;}
/* libxkbcommon - never called headless; versioned at link time via xkb.map */
void *xkb_compose_state_feed(void){return 0;} void *xkb_compose_state_get_status(void){return 0;}
void *xkb_compose_state_get_utf8(void){return 0;} void *xkb_compose_state_new(void){return 0;}
void *xkb_compose_state_reset(void){return 0;} void *xkb_compose_state_unref(void){return 0;}
void *xkb_compose_table_new_from_locale(void){return 0;} void *xkb_compose_table_unref(void){return 0;}
void *xkb_context_new(void){return 0;} void *xkb_context_unref(void){return 0;}
void *xkb_keymap_key_repeats(void){return 0;} void *xkb_keymap_mod_get_index(void){return 0;}
void *xkb_keymap_new_from_string(void){return 0;} void *xkb_keymap_unref(void){return 0;}
void *xkb_state_get_keymap(void){return 0;} void *xkb_state_key_get_one_sym(void){return 0;}
void *xkb_state_key_get_utf8(void){return 0;} void *xkb_state_new(void){return 0;}
void *xkb_state_serialize_mods(void){return 0;} void *xkb_state_unref(void){return 0;}
void *xkb_state_update_mask(void){return 0;}
EOF
  gcc -shared -fPIC -o "$STUBS/libXfixes.so.3" -Wl,-soname,libXfixes.so.3 "$STUBS/stubs.c"
  gcc -shared -fPIC -o "$STUBS/libXi.so.6"     -Wl,-soname,libXi.so.6     "$STUBS/stubs.c"
  for n in libXrender.so.1 libSM.so.6 libICE.so.6 libGL.so.1; do
    gcc -shared -fPIC -o "$STUBS/$n" -Wl,-soname,$n "$STUBS/stubs.c"
  done
  # the xkb symbols must carry the V_0.5.0 version node the bpy wheel asks for
  cat > "$STUBS/xkb.map" <<'EOF'
V_0.5.0 {
  global: xkb_*;
  local: *;
};
EOF
  gcc -shared -fPIC -o "$STUBS/libxkbcommon.so.0" -Wl,-soname,libxkbcommon.so.0 \
      -Wl,--version-script="$STUBS/xkb.map" "$STUBS/stubs.c"
fi

echo "WORLD KIT toolchain ready:"
echo "  venv : $VENV"
echo "  stubs: $STUBS"
echo "Run with:  LD_LIBRARY_PATH=$STUBS $VENV/bin/python tools/wk.py --stage all"
