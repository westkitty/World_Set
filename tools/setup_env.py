#!/usr/bin/env python3
"""Recreate the headless runtime for `bpy` on a box with no X libraries.

The sandbox image has no libGL / libX* / libxkbcommon and no apt access, but
Blender-as-a-module links them even though background Cycles rendering never
touches a window system. This generates tiny stub shared libraries exporting
exactly the symbols (including versioned ones) that bpy asks for, so the
dynamic loader is satisfied and `import bpy` works.

    python3 tools/setup_env.py            # writes ~/stublibs
    export LD_LIBRARY_PATH=~/stublibs     # then `import bpy` works

`tools/wk.sh <script.py>` does both for you.
"""
import os
import re
import subprocess
import sys
from collections import defaultdict

OUT = os.path.expanduser('~/stublibs')
BPY = '/usr/local/lib/python3.11/dist-packages/bpy'

GROUPS = [
    ('libGL.so.1',        (r'^gl[A-Z]', r'^glX', r'^glew')),
    ('libXrender.so.1',   (r'^XRender',)),
    ('libXfixes.so.3',    (r'^XFixes',)),
    ('libXi.so.6',        (r'^XI[A-Z]', r'^XOpenDevice', r'^XCloseDevice',
                           r'^XListInputDevices', r'^XFreeDeviceList',
                           r'^XSelectExtensionEvent', r'^XGetExtensionVersion',
                           r'^XQueryDeviceState', r'^XFreeDeviceState',
                           r'^XGetDeviceButtonMapping', r'^XDeviceInfo', r'^_Xi', r'^XChangeDeviceDontPropagateList', r'^XGetDeviceMotionEvents')),
    ('libICE.so.6',       (r'^Ice',)),
    ('libSM.so.6',        (r'^Sm',)),
    ('libxkbcommon.so.0', (r'^xkb_',)),
]


def undefined_symbols(root):
    """Every undefined symbol across bpy's own shared objects."""
    sos = []
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            if '.so' in fn:
                sos.append(os.path.join(dirpath, fn))
    syms = []
    for so in sos:
        out = subprocess.run(['nm', '-D', '--undefined-only', so],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[-2] in ('U', 'w'):
                syms.append(parts[-1])
    return sorted(set(syms))


def build(lib, syms):
    """syms: list of raw names, possibly 'name@VERSION'."""
    stem = os.path.join(OUT, lib.replace('.', '_'))
    versions = defaultdict(list)
    plain = []
    seen = set()
    for s in syms:
        base, _, ver = s.partition('@')
        base = base.strip()
        if base in seen:
            continue
        seen.add(base)
        if ver:
            versions[ver.lstrip('@')].append(base)
        else:
            plain.append(base)
    src = stem + '.c'
    with open(src, 'w') as f:
        f.write('/* WORLD KIT generated stub for %s */\n' % lib)
        for b in plain + [b for v in versions.values() for b in v]:
            f.write('void %s(void) {}\n' % b)
        if not seen:
            f.write('void __worldkit_stub_marker(void) {}\n')
    args = ['gcc', '-shared', '-fPIC', '-o', os.path.join(OUT, lib), src,
            '-Wl,-soname,' + lib]
    if versions:
        mapf = stem + '.map'
        with open(mapf, 'w') as f:
            for ver, names in versions.items():
                f.write('%s {\n  global:\n' % ver)
                for n in names:
                    f.write('    %s;\n' % n)
                f.write('};\n')
        args.append('-Wl,--version-script=' + mapf)
    subprocess.run(args, check=True)
    return len(seen)


def main():
    os.makedirs(OUT, exist_ok=True)
    syms = undefined_symbols(BPY)
    for lib, pats in GROUPS:
        rx = [re.compile(p) for p in pats]
        mine = [s for s in syms if any(r.match(s) for r in rx)]
        n = build(lib, mine)
        print('%-22s %4d symbols' % (lib, n))
    env = dict(os.environ, LD_LIBRARY_PATH=OUT)
    r = subprocess.run([sys.executable, '-c',
                        'import bpy; print("OK bpy", bpy.app.version_string)'],
                       env=env, capture_output=True, text=True)
    tail = (r.stdout + r.stderr).strip().splitlines()
    print(tail[-1] if tail else '(no output)')
    return 0 if r.returncode == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
