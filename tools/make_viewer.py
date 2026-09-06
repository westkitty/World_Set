#!/usr/bin/env python3
"""Build the WORLD KIT interactive viewer.

Reads every exported GLB (no Blender needed), derives bounding boxes, material
lists and triangle counts straight out of the glTF JSON chunk, then writes
    WorldKit/viewer/assets.json
    WorldKit/viewer/index.html
The renderer itself lives in WorldKit/viewer/glb.js (hand-written WebGL).
"""
import json
import math
import os
import struct

ROOT = '/home/user/World_Set/WorldKit'
GLB = os.path.join(ROOT, 'glb')
VIEW = os.path.join(ROOT, 'viewer')
os.makedirs(VIEW, exist_ok=True)

CATS = ['WK_ARCH', 'WK_STR', 'WK_DOOR', 'WK_WND', 'WK_WALL', 'WK_FLR', 'WK_TER',
        'WK_FUR', 'WK_PRP', 'WK_LGT', 'WK_SGN', 'WK_VEG', 'WK_DCL', 'WK_HERO']
CATNAMES = {'WK_ARCH': 'ARCHITECTURE', 'WK_STR': 'STRUCTURAL', 'WK_DOOR': 'DOORS',
            'WK_WND': 'WINDOWS', 'WK_WALL': 'WALLS', 'WK_FLR': 'FLOORS',
            'WK_TER': 'TERRAIN', 'WK_FUR': 'FURNITURE', 'WK_PRP': 'PROPS',
            'WK_LGT': 'LIGHTS', 'WK_SGN': 'SIGNAGE', 'WK_VEG': 'VEGETATION',
            'WK_DCL': 'DECALS', 'WK_HERO': 'HERO OBJECTS'}


# ----------------------------------------------------------------- glb utils
def read_glb_json(path):
    with open(path, 'rb') as f:
        data = f.read()
    assert data[:4] == b'glTF', path
    off, js = 12, None
    while off < len(data):
        ln, ty = struct.unpack_from('<II', data, off)
        if ty == 0x4E4F534A:
            js = json.loads(data[off + 8:off + 8 + ln].decode('utf-8'))
            break
        off += 8 + ln + (-ln % 4)
    return js, len(data)


def mat_mul(a, b):
    return [sum(a[k * 4 + r] * b[c * 4 + k] for k in range(4))
            for c in range(4) for r in range(4)]


def trs(t, q, s):
    x, y, z, w = q
    x2, y2, z2 = x + x, y + y, z + z
    xx, xy, xz = x * x2, x * y2, x * z2
    yy, yz, zz = y * y2, y * z2, z * z2
    wx, wy, wz = w * x2, w * y2, w * z2
    return [(1 - (yy + zz)) * s[0], (xy + wz) * s[0], (xz - wy) * s[0], 0,
            (xy - wz) * s[1], (1 - (xx + zz)) * s[1], (yz + wx) * s[1], 0,
            (xz + wy) * s[2], (yz - wx) * s[2], (1 - (xx + yy)) * s[2], 0,
            t[0], t[1], t[2], 1]


def apply(m, p):
    return [m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12],
            m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13],
            m[2] * p[0] + m[6] * p[1] + m[10] * p[2] + m[14]]


def analyse(js):
    lo = [1e9] * 3
    hi = [-1e9] * 3
    tris = 0
    mats = set()
    ident = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

    def visit(ni, parent):
        nonlocal tris
        n = js['nodes'][ni]
        local = n['matrix'] if 'matrix' in n else trs(n.get('translation', [0, 0, 0]),
                                                      n.get('rotation', [0, 0, 0, 1]),
                                                      n.get('scale', [1, 1, 1]))
        world = mat_mul(parent, local)
        if 'mesh' in n:
            for pr in js['meshes'][n['mesh']]['primitives']:
                acc = js['accessors'][pr['attributes']['POSITION']]
                mn, mx = acc['min'], acc['max']
                for bit in range(8):
                    p = apply(world, [(mx if bit & 1 else mn)[0],
                                      (mx if bit & 2 else mn)[1],
                                      (mx if bit & 4 else mn)[2]])
                    for k in range(3):
                        lo[k] = min(lo[k], p[k])
                        hi[k] = max(hi[k], p[k])
                if 'indices' in pr:
                    tris += js['accessors'][pr['indices']]['count'] // 3
                else:
                    tris += acc['count'] // 3
                if 'material' in pr:
                    mats.add(js['materials'][pr['material']].get('name', 'material'))
        for c in n.get('children', []):
            visit(c, world)

    for ni in js['scenes'][js.get('scene', 0)]['nodes']:
        visit(ni, ident)
    return lo, hi, tris, sorted(mats)


# ----------------------------------------------------------------- gather
stats = {s['name']: s for s in json.load(open('/home/user/World_Set/work/asset_stats.json'))}
assets = []
for name in sorted(stats):
    path = os.path.join(GLB, name + '.glb')
    if not os.path.exists(path):
        print('missing glb', name)
        continue
    js, size = read_glb_json(path)
    lo, hi, tris, mats = analyse(js)
    cat = '_'.join(name.split('_')[:2])
    st = stats[name]
    # glTF is Y-up: x=width, y=height, z=depth(blender Y)
    assets.append({
        'name': name, 'cat': cat, 'catname': CATNAMES[cat],
        'label': name.split('_', 2)[2],
        'tris': tris, 'parts': st['parts'], 'lights': st['lights'],
        'kb': round(size / 1024),
        'dim': [round(hi[0] - lo[0], 2), round(hi[2] - lo[2], 2), round(hi[1] - lo[1], 2)],
        'base': [round((lo[0] + hi[0]) / 2, 3), round((lo[2] + hi[2]) / 2, 3), round(lo[1], 3)],
        'mats': mats,
    })
assets.sort(key=lambda a: (CATS.index(a['cat']), a['name']))

show = {}
sp = '/home/user/World_Set/work/showcase_stats.json'
if os.path.exists(sp):
    show = json.load(open(sp))
ex = show.get('extent', {'x': [-43, 43], 'y': [-18, 45]})
footprint = '%d × %d m' % (ex['x'][1] - ex['x'][0], ex['y'][1] - ex['y'][0])

meta = {
    'title': 'WORLD KIT — STARLIGHT ESTATES',
    'concept': '1995 trailer park at night',
    'assets': assets,
    'cats': [{'id': c, 'name': CATNAMES[c],
              'n': sum(1 for a in assets if a['cat'] == c)} for c in CATS],
    'totals': {'assets': len(assets), 'tris': sum(a['tris'] for a in assets),
               'mats': len(set(m for a in assets for m in a['mats'])),
               'instances': show.get('instances', 0),
               'lights': show.get('spill_lights', 0) + sum(a['lights'] for a in assets
                                                           if a['lights']) * 0,
               'footprint': footprint},
    'showcase': show,
}
json.dump(meta, open(os.path.join(VIEW, 'assets.json'), 'w'), indent=1)
print('assets.json', len(assets), 'assets', meta['totals'])

# ----------------------------------------------------------------- html
HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WORLD KIT — Starlight Estates · Interactive Kit Viewer</title>
<style>
:root{
  --bg:#080b12; --panel:#0e131d; --panel2:#131a27; --line:#20293b;
  --ink:#e9e3d5; --dim:#8d9ab2; --hot:#ffb43f; --neon:#ff5b6e; --cool:#6fd0ff;
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font:14px/1.45 ui-sans-serif,system-ui,"Segoe UI",Roboto,sans-serif;overflow:hidden}
header{display:flex;align-items:center;gap:18px;padding:10px 18px;background:linear-gradient(#121a27,#0b101a);
  border-bottom:1px solid var(--line)}
header h1{font-size:15px;letter-spacing:.16em;margin:0;font-weight:700}
header h1 b{color:var(--hot)}
header .tag{color:var(--dim);font-size:12px;letter-spacing:.05em}
nav{margin-left:auto;display:flex;gap:6px}
nav button{background:#131a27;border:1px solid var(--line);color:var(--dim);padding:6px 14px;
  border-radius:999px;font-size:12px;letter-spacing:.08em;cursor:pointer}
nav button.on{background:var(--hot);border-color:var(--hot);color:#20160a;font-weight:700}
main{height:calc(100vh - 47px);display:none}
main.on{display:flex}
/* ---- kit browser ---- */
#side{width:314px;flex:none;background:var(--panel);border-right:1px solid var(--line);
  display:flex;flex-direction:column}
#search{margin:12px;padding:8px 10px;background:#080c14;border:1px solid var(--line);
  border-radius:8px;color:var(--ink);font-size:13px}
#chips{display:flex;flex-wrap:wrap;gap:5px;padding:0 12px 10px}
#chips span{font-size:10.5px;letter-spacing:.07em;padding:3px 8px;border-radius:999px;
  background:#141b29;border:1px solid var(--line);color:var(--dim);cursor:pointer;white-space:nowrap}
#chips span.on{background:#26314a;color:#ffe6bd;border-color:#3a4counts}
#chips span.on{border-color:var(--hot);color:var(--hot)}
#list{overflow:auto;flex:1;padding:0 8px 16px}
.item{display:flex;gap:10px;align-items:center;padding:6px;border-radius:9px;cursor:pointer;
  border:1px solid transparent}
.item:hover{background:#131b28}
.item.on{background:#1b2436;border-color:#31405e}
.item img{width:52px;height:52px;border-radius:6px;background:#05070c;flex:none;object-fit:cover}
.item .n{font-size:12.5px;font-weight:600;color:#ffeccd}
.item .m{font-size:11px;color:var(--dim)}
.catbar{position:sticky;top:0;background:linear-gradient(#0e131d,#0e131de0);padding:9px 6px 5px;
  font-size:10.5px;letter-spacing:.18em;color:var(--cool);z-index:2}
/* ---- stage ---- */
#stage{flex:1;display:flex;flex-direction:column;min-width:0}
#canwrap{flex:1;position:relative;background:radial-gradient(80% 80% at 50% 40%,#121a26,#05070c 75%)}
canvas{width:100%;height:100%;display:block;touch-action:none;cursor:grab}
canvas:active{cursor:grabbing}
#nowebgl{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:10px;color:var(--dim);font-size:12px;letter-spacing:.08em}
#nowebgl img{max-width:62%;max-height:66%;border:1px solid var(--line);border-radius:10px}
#nowebgl b{color:var(--ink)}
#tools{position:absolute;left:14px;top:14px;display:flex;gap:6px;flex-wrap:wrap}
#tools button{background:#0f1622cc;border:1px solid var(--line);color:var(--dim);
  padding:6px 11px;border-radius:7px;font-size:11.5px;cursor:pointer;backdrop-filter:blur(4px)}
#tools button.on{border-color:var(--hot);color:var(--hot)}
#hud{position:absolute;right:14px;top:14px;text-align:right;font-size:11.5px;color:var(--dim);
  background:#0b1119aa;border:1px solid var(--line);border-radius:8px;padding:8px 11px;
  backdrop-filter:blur(4px)}
#hud b{color:#ffe0a8;font-weight:600}
#title{position:absolute;left:14px;bottom:12px}
#title .t{font-size:19px;font-weight:700;color:#fff1d8;letter-spacing:.02em}
#title .s{font-size:12px;color:var(--dim);letter-spacing:.1em}
#meta{flex:none;height:170px;border-top:1px solid var(--line);background:var(--panel);
  display:grid;grid-template-columns:repeat(4,1fr);gap:1px;overflow:hidden}
.mcell{background:var(--panel2);padding:12px 16px;overflow:auto}
.mcell h4{margin:0 0 7px;font-size:10.5px;letter-spacing:.16em;color:var(--cool);font-weight:600}
.mcell .big{font-size:20px;color:#ffe0a8;font-weight:700}
.mcell .row{display:flex;justify-content:space-between;font-size:12px;color:var(--dim);
  border-bottom:1px dotted #232c3f;padding:2px 0}
.mcell .row b{color:var(--ink);font-weight:600}
.pill{display:inline-block;font-size:11px;padding:2px 7px;margin:2px 3px 0 0;border-radius:5px;
  background:#1a2333;color:#c7d3e8;border:1px solid #26314a}
a.dl{color:var(--hot);text-decoration:none;font-size:12px}
/* ---- scene tab ---- */
#scene{padding:18px;overflow:auto;width:100%}
#scene h2{font-size:12px;letter-spacing:.2em;color:var(--cool);margin:18px 0 8px}
.shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:14px}
.shots figure{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:11px;overflow:hidden}
.shots img{width:100%;display:block;background:#05070c}
.shots figcaption{padding:8px 12px;font-size:11.5px;color:var(--dim);letter-spacing:.06em}
#panowrap{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:11px;
  height:330px;background:#05070c;cursor:ew-resize}
#panocv{position:absolute;inset:0;width:100%;height:100%;display:block;cursor:grab;
  touch-action:none;background:#05070c}
#panocv:active{cursor:grabbing}
#panohint{position:absolute;left:12px;bottom:10px;font-size:11px;letter-spacing:.08em;
  color:var(--dim);background:#0b1119aa;border:1px solid var(--line);border-radius:7px;
  padding:5px 9px;pointer-events:none}
#panoimg{display:none;position:absolute;top:0;left:0;height:100%;max-width:none;user-select:none;
  -webkit-user-drag:none}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 2px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:9px 15px;min-width:120px}
.stat .v{font-size:20px;font-weight:700;color:#ffe0a8}
.stat .k{font-size:10.5px;letter-spacing:.14em;color:var(--dim)}
video{width:100%;max-width:1100px;border:1px solid var(--line);border-radius:11px;background:#000}
.note{color:var(--dim);font-size:12.5px;max-width:1100px}
.note code{color:#ffd79a;background:#141c2a;padding:1px 5px;border-radius:4px}
</style></head><body>

<header>
  <h1>WORLD <b>KIT</b></h1>
  <span class="tag">STARLIGHT ESTATES · 1995 TRAILER PARK AT NIGHT</span>
  <nav>
    <button data-tab="kit" class="on">KIT BROWSER</button>
    <button data-tab="scene">SHOWCASE</button>
    <button data-tab="walk">WALKTHROUGH</button>
  </nav>
</header>

<main id="kit" class="on">
  <aside id="side">
    <input id="search" placeholder="search assets…">
    <div id="chips"></div>
    <div id="list"></div>
  </aside>
  <section id="stage">
    <div id="canwrap">
      <canvas id="cv"></canvas>
      <div id="tools">
        <button id="bspin" class="on">AUTO-SPIN</button>
        <button id="bgrid" class="on">GRID + ORIGIN</button>
        <button id="bwire">WIREFRAME</button>
        <button id="bfit">RESET VIEW</button>
      </div>
      <div id="hud"></div>
      <div id="title"><div class="t" id="tt">—</div><div class="s" id="ts">—</div></div>
    </div>
    <div id="meta">
      <div class="mcell"><h4>ASSET</h4><div id="m1"></div></div>
      <div class="mcell"><h4>BOUNDS &amp; ORIGIN</h4><div id="m2"></div></div>
      <div class="mcell"><h4>MATERIALS</h4><div id="m3"></div></div>
      <div class="mcell"><h4>PIPELINE</h4><div id="m4"></div></div>
    </div>
  </section>
</main>

<main id="scene"><div style="width:100%">
  <div class="stats" id="sstats"></div>
  <h2>HERO RENDERS · CYCLES 1920×1080</h2>
  <div class="shots" id="shots"></div>
  <h2>360° ENVIRONMENT PANORAMA · EQUIRECTANGULAR · DRAG TO PAN</h2>
  <div id="panowrap"><canvas id="panocv"></canvas><img id="panoimg" src="../renders/pano_360.png" alt="360 panorama"><div id="panohint">drag to look · scroll to zoom · double-click to stop the drift</div></div>
  <h2>THE KIT IN THE SCENE</h2>
  <p class="note">Everything in these frames is an instance of the same __N__ library assets —
  no bespoke geometry was modelled for the shot. Assets are linked as collection instances, so
  editing a kit piece updates every copy in the park.</p>
</div></main>

<main id="walk"><div style="padding:18px;overflow:auto;width:100%">
  <h2 style="font-size:12px;letter-spacing:.2em;color:var(--cool);margin:6px 0 10px">
    CAMERA WALKTHROUGH · MAIN STREET → SUNSET COURT → CRANE</h2>
  <video src="../video/walkthrough.mp4" controls autoplay muted loop playsinline></video>
  <p class="note" style="margin-top:14px">Single continuous dolly: the camera rolls east down
  Main Street past the marquee and the single-wides, turns north into Sunset Court alongside the
  laundromat, then cranes up over Sunset Row. Catmull-Rom position/target/lens splines with an
  ease-in-out time curve and a light hand-held float.</p>
</div></main>

<script src="glb.js"></script>
<script>
const S = {data:null, cur:null, cat:'ALL', q:''};
const $ = s => document.querySelector(s);

document.querySelectorAll('nav button').forEach(b => b.onclick = () => {
  document.querySelectorAll('nav button').forEach(x => x.classList.toggle('on', x === b));
  document.querySelectorAll('main').forEach(m => m.classList.toggle('on', m.id === b.dataset.tab));
});

// The live 3D panel is a bonus: if the browser has no WebGL2 (headless,
// blocked GPU, ancient browser) everything else must still work, so fall back
// to a no-op stand-in and let the rendered thumbnail carry the preview.
let V, WEBGL = true;
try {
  V = WKViewer.create($('#cv'));
} catch (err) {
  WEBGL = false;
  console.warn('3D preview unavailable:', err && err.message);
  V = {spin: false, grid: false, wire: false, yaw: 0, pitch: 0, dist: 4,
       target: [0, 0, 0], onspin: null, load: () => Promise.resolve(null)};
  $('#cv').style.display = 'none';
  const note = document.createElement('div');
  note.id = 'nowebgl';
  note.innerHTML = '<img id="nogl_img" alt=""><div><b>WebGL2 unavailable</b> — ' +
                   'showing the rendered thumbnail</div>';
  $('#canwrap').appendChild(note);
}
V.onspin = on => $('#bspin').classList.toggle('on', on);
$('#bspin').onclick = e => { V.spin = !V.spin; e.target.classList.toggle('on', V.spin); };
$('#bgrid').onclick = e => { V.grid = !V.grid; e.target.classList.toggle('on', V.grid); };
$('#bwire').onclick = e => { V.wire = !V.wire; e.target.classList.toggle('on', V.wire); };
$('#bfit').onclick = () => { V.yaw = 0.9; V.pitch = 0.42; if (S.cur) fit(S.cur); };

function fit(a){ const d = a.dim; V.dist = Math.max(d[0], d[1], d[2]) * 1.85 + 0.6;
  V.target = [0, d[2] * 0.45, 0]; }

function chips(){
  const c = $('#chips'); c.innerHTML = '';
  const all = document.createElement('span');
  all.textContent = 'ALL ' + S.data.totals.assets; all.className = S.cat === 'ALL' ? 'on' : '';
  all.onclick = () => { S.cat = 'ALL'; chips(); list(); }; c.appendChild(all);
  S.data.cats.forEach(k => { if (!k.n) return;
    const s = document.createElement('span');
    s.textContent = k.name + ' ' + k.n; s.className = S.cat === k.id ? 'on' : '';
    s.onclick = () => { S.cat = k.id; chips(); list(); }; c.appendChild(s); });
}

function list(){
  const L = $('#list'); L.innerHTML = ''; let last = '';
  S.data.assets.filter(a => (S.cat === 'ALL' || a.cat === S.cat) &&
      (!S.q || a.name.toLowerCase().includes(S.q))).forEach(a => {
    if (a.catname !== last){ last = a.catname;
      const h = document.createElement('div'); h.className = 'catbar'; h.textContent = last;
      L.appendChild(h); }
    const d = document.createElement('div');
    d.className = 'item' + (S.cur && S.cur.name === a.name ? ' on' : '');
    d.innerHTML = `<img loading="lazy" src="../catalog/thumbs/${a.name}.png">
      <div><div class="n">${a.label}</div>
      <div class="m">${a.tris} tris · ${a.parts} parts${a.lights ? ' · ' + a.lights + ' light' : ''}</div></div>`;
    d.onclick = () => select(a);
    L.appendChild(d);
  });
}

async function select(a){
  S.cur = a; list();
  $('#tt').textContent = a.label;
  $('#ts').textContent = a.catname + ' · ' + a.name;
  $('#hud').innerHTML = 'loading…';
  $('#m1').innerHTML =
    `<div class="big">${a.tris.toLocaleString()} tris</div>
     <div class="row"><span>parts</span><b>${a.parts}</b></div>
     <div class="row"><span>baked lights</span><b>${a.lights}</b></div>
     <div class="row"><span>glb size</span><b>${a.kb} KB</b></div>`;
  $('#m2').innerHTML =
    `<div class="row"><span>width (X)</span><b>${a.dim[0]} m</b></div>
     <div class="row"><span>depth (Y)</span><b>${a.dim[1]} m</b></div>
     <div class="row"><span>height (Z)</span><b>${a.dim[2]} m</b></div>
     <div class="row"><span>origin</span><b>base centre, z = 0</b></div>
     <div class="row"><span>front faces</span><b>+Y</b></div>`;
  $('#m3').innerHTML = a.mats.map(m => `<span class="pill">${m}</span>`).join('');
  $('#m4').innerHTML =
    `<div class="row"><span>naming</span><b>WK_&lt;CAT&gt;_&lt;Name&gt;</b></div>
     <div class="row"><span>parts / lights</span><b>_P## / _L##</b></div>
     <div class="row"><span>scale</span><b>1 unit = 1 m</b></div>
     <div style="margin-top:8px"><a class="dl" href="../glb/${a.name}.glb" download>↓ download ${a.name}.glb</a></div>`;
  fit(a);
  if (!WEBGL) {
    const im = $('#nogl_img');
    if (im) im.src = '../catalog/thumbs/' + a.name + '.png';
    $('#hud').innerHTML = `<b>${a.tris.toLocaleString()}</b> triangles<br>` +
      `<b>${a.parts}</b> parts · <b>${a.mats.length}</b> materials<br>` +
      `<b>${a.dim[0]}×${a.dim[1]}×${a.dim[2]}</b> m`;
    return;
  }
  try {
    const st = await V.load('../glb/' + a.name + '.glb');
    $('#hud').innerHTML = `<b>${st.tris.toLocaleString()}</b> triangles<br>` +
      `<b>${st.prims}</b> draw parts · <b>${a.mats.length}</b> materials<br>` +
      `<b>${a.dim[0]}×${a.dim[1]}×${a.dim[2]}</b> m`;
  } catch (e) {
    $('#hud').innerHTML = 'GLB load failed — serve this folder over http<br>' +
      '<code>python3 -m http.server</code>';
  }
}

$('#search').oninput = e => { S.q = e.target.value.trim().toLowerCase(); list(); };

// ---- 360 panorama: true equirect projection in WebGL, flat drag-pan fallback
(function(){
  try {
    WKViewer.pano($('#panocv'), '../renders/pano_360.png');
    return;
  } catch (err) {
    console.warn('equirect viewer unavailable:', err && err.message);
  }
  $('#panocv').style.display = 'none';
  const w = $('#panowrap'), im = $('#panoimg');
  im.style.display = 'block';
  $('#panohint').textContent = 'drag to pan (flat fallback — no WebGL2)';
  let down = false, x0 = 0, sl = 0;
  w.addEventListener('pointerdown', e => { down = true; x0 = e.clientX; sl = im.offsetLeft; });
  addEventListener('pointerup', () => down = false);
  w.addEventListener('pointermove', e => {
    if (!down) return;
    const min = w.clientWidth - im.clientWidth;
    im.style.left = Math.max(min, Math.min(0, sl + (e.clientX - x0))) + 'px';
  });
  setInterval(() => {
    if (down) return;
    const min = w.clientWidth - im.clientWidth;
    let l = im.offsetLeft - 0.5;
    if (l < min) l = 0;
    im.style.left = l + 'px';
  }, 40);
})();

const SHOTS = [
  ['showcase_hero.png', 'HERO · the marquee at the west entry, 26 mm'],
  ['showcase_street.png', 'MAIN STREET · looking west from the junction, 40 mm'],
  ['showcase_court.png', 'SUNSET COURT · laundromat, neon + vending, 35 mm'],
  ['showcase_yard.png', 'LOT 6 · boarded window, screen door, pickup, 30 mm'],
  ['showcase_fire.png', 'BURN BARREL · TV-lit glass and warm glass, 35 mm'],
  ['showcase_aerial.png', 'AERIAL · the whole plan from the south-west, 24 mm']
];

fetch('assets.json').then(r => r.json()).then(d => {
  S.data = d; chips(); list(); select(d.assets[0]);
  const t = d.totals;
  $('#sstats').innerHTML = [
    [t.assets, 'KIT ASSETS'], [t.tris.toLocaleString(), 'KIT TRIANGLES'],
    [t.mats, 'MATERIALS'], [t.instances || '—', 'SCENE INSTANCES'],
    [t.lights || '—', 'WINDOW SPILL LIGHTS'], [t.footprint, 'PARK FOOTPRINT']
  ].map(s => `<div class="stat"><div class="v">${s[0]}</div><div class="k">${s[1]}</div></div>`).join('');
  $('#shots').innerHTML = SHOTS.map(s =>
    `<figure><img loading="lazy" src="../renders/${s[0]}"><figcaption>${s[1]}</figcaption></figure>`).join('');
});
</script>
</body></html>
"""

HTML = HTML.replace('__N__', str(len(assets)))
open(os.path.join(VIEW, 'index.html'), 'w').write(HTML)
print('index.html written ->', os.path.join(VIEW, 'index.html'))

# ------------------------------------------------------------ landing page
LANDING = """<!DOCTYPE html><meta charset="utf-8">
<title>WORLD KIT — Starlight Estates</title>
<meta http-equiv="refresh" content="0; url=viewer/index.html">
<body style="background:#080b12;color:#e9e3d5;font:14px system-ui;padding:40px">
Loading the <a style="color:#ffb43f" href="viewer/index.html">WORLD KIT viewer</a>…
</body>"""
open(os.path.join(ROOT, 'index.html'), 'w').write(LANDING)
print('landing page written')
