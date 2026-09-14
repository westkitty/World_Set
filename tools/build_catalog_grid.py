import os
import json
from PIL import Image, ImageDraw, ImageFont

THUMBS_DIR = "/Users/andrew/World_Set/renders/catalog/thumbnails"
OUTPUT_GRID = "/Users/andrew/World_Set/renders/catalog/catalog_grid.png"
HTML_OUTPUT = "/Users/andrew/World_Set/renders/catalog/index.html"
MANIFEST_PATH = "/Users/andrew/World_Set/ASSET_MANIFEST.json"

with open(MANIFEST_PATH, "r") as f:
    manifest = json.load(f)

assets = manifest["assets"]
assets.sort(key=lambda x: (x["category"], x["name"]))

# 1. Build Visual Catalog Grid Image
cell_w, cell_h = 320, 360
thumb_size = 320
cols = 6
rows = math = (len(assets) + cols - 1) // cols

grid_w = cols * cell_w + 40
grid_h = rows * cell_h + 120

grid_img = Image.new("RGB", (grid_w, grid_h), (20, 24, 28))
draw = ImageDraw.Draw(grid_img)

# Title Header
draw.rectangle([(0, 0), (grid_w, 80)], fill=(12, 15, 18))
draw.text((30, 20), "WORLD KIT — SITE-44 ASSET VOCABULARY CATALOG", fill=(245, 183, 0))
draw.text((30, 48), f"Production Modular Library: {len(assets)} Verified Assets across 10 Categories | Format: GLB / PBR", fill=(160, 175, 185))

for idx, asset in enumerate(assets):
    c = idx % cols
    r = idx // cols
    x = 20 + c * cell_w
    y = 100 + r * cell_h
    
    # Cell background border
    draw.rectangle([(x, y), (x + cell_w - 10, y + cell_h - 10)], fill=(28, 33, 38), outline=(45, 52, 60), width=1)
    
    # Load thumbnail
    thumb_path = os.path.join(THUMBS_DIR, f"{asset['name']}.png")
    if os.path.exists(thumb_path):
        t_img = Image.open(thumb_path).resize((cell_w - 12, cell_w - 12))
        grid_img.paste(t_img, (x + 1, y + 1))
        
    # Label bar
    bar_y = y + cell_w - 10
    draw.rectangle([(x + 1, bar_y), (x + cell_w - 11, y + cell_h - 11)], fill=(16, 20, 24))
    # Category tag
    draw.text((x + 8, bar_y + 4), f"[{asset['category'].upper()}]", fill=(27, 231, 255))
    # Asset Name
    name_short = asset['name']
    if len(name_short) > 22:
        name_short = name_short[:20] + "..."
    draw.text((x + 8, bar_y + 20), name_short, fill=(240, 245, 250))
    # Dimensions
    dim_str = f"{asset['dimensions_m'][0]}x{asset['dimensions_m'][1]}x{asset['dimensions_m'][2]}m | {asset['polygons']}P"
    draw.text((x + 8, bar_y + 35), dim_str, fill=(140, 150, 160))

grid_img.save(OUTPUT_GRID)
print(f"Generated visual catalog grid: {OUTPUT_GRID} ({grid_w}x{grid_h})")

# 2. Build Interactive Standalone HTML Catalog Viewer
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>WORLD KIT — Site-44 Modular Environment Library</title>
<style>
  :root {{
    --bg-dark: #0f1115;
    --card-bg: #181c22;
    --card-border: #262c36;
    --accent-yellow: #f5b700;
    --accent-cyan: #1be7ff;
    --text-main: #e2e8f0;
    --text-muted: #94a3b8;
  }}
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace, sans-serif;
    background-color: var(--bg-dark);
    color: var(--text-main);
    line-height: 1.5;
  }}
  header {{
    padding: 2.5rem 3rem 1.5rem;
    background: linear-gradient(180deg, #161a22 0%, #0f1115 100%);
    border-bottom: 2px solid var(--accent-yellow);
  }}
  h1 {{ margin: 0 0 0.5rem 0; font-size: 2rem; color: var(--accent-yellow); letter-spacing: 1px; }}
  .subtitle {{ color: var(--text-muted); font-size: 1.1rem; max-width: 900px; }}
  .nav-tabs {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1.5rem; }}
  .tab-btn {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    color: var(--text-main);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.2s;
  }}
  .tab-btn:hover, .tab-btn.active {{
    background: var(--accent-yellow);
    color: #000;
    border-color: var(--accent-yellow);
  }}
  .section-title {{
    padding: 1.5rem 3rem 0.5rem;
    font-size: 1.4rem;
    color: var(--accent-cyan);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .gallery-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
    gap: 1.5rem;
    padding: 1rem 3rem 2.5rem;
  }}
  .gallery-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 6px;
    overflow: hidden;
  }}
  .gallery-card img, .gallery-card video {{
    width: 100%;
    height: auto;
    display: block;
  }}
  .gallery-info {{
    padding: 1rem;
  }}
  .gallery-info h3 {{ margin: 0 0 0.25rem; font-size: 1.1rem; color: var(--accent-yellow); }}
  .gallery-info p {{ margin: 0; color: var(--text-muted); font-size: 0.9rem; }}
  
  .asset-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    padding: 1rem 3rem 4rem;
  }}
  .asset-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 6px;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
  }}
  .asset-card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent-cyan);
  }}
  .asset-thumb {{
    width: 100%;
    aspect-ratio: 1/1;
    background: #08090b;
    object-fit: contain;
    display: block;
  }}
  .asset-body {{
    padding: 1rem;
  }}
  .badge {{
    display: inline-block;
    padding: 0.2rem 0.5rem;
    font-size: 0.75rem;
    font-weight: 700;
    border-radius: 3px;
    text-transform: uppercase;
    background: #222b35;
    color: var(--accent-cyan);
    margin-bottom: 0.5rem;
  }}
  .asset-name {{
    font-size: 0.95rem;
    font-weight: 700;
    margin: 0 0 0.5rem;
    word-break: break-all;
    color: #fff;
  }}
  .specs-table {{
    width: 100%;
    font-size: 0.8rem;
    color: var(--text-muted);
    border-collapse: collapse;
    margin-bottom: 0.75rem;
  }}
  .specs-table td {{ padding: 2px 0; }}
  .specs-table td:first-child {{ color: #64748b; width: 45%; }}
  .download-btn {{
    display: block;
    text-align: center;
    background: #1e2630;
    border: 1px solid var(--card-border);
    color: var(--accent-cyan);
    padding: 0.4rem 0.75rem;
    border-radius: 4px;
    text-decoration: none;
    font-size: 0.8rem;
    font-weight: 600;
    transition: background 0.2s;
  }}
  .download-btn:hover {{
    background: var(--accent-cyan);
    color: #000;
  }}
</style>
</head>
<body>

<header>
  <h1>WORLD KIT — SITE-44 SUB-AQUIFER RESEARCH COMPLEX</h1>
  <div class="subtitle">
    Monolithic Brutalist Retro-Industrial Subterranean Environment Generation Language.<br>
    {len(assets)} Reusable Precision Modular Production Assets, 7 PBR Material Families, Master Assembly &amp; Renders.
  </div>
  <div class="nav-tabs" id="filters">
    <button class="tab-btn active" onclick="filterCategory('all')">ALL ASSETS ({len(assets)})</button>
"""

categories = sorted(list(set(a["category"] for a in assets)))
for cat in categories:
    cat_count = sum(1 for a in assets if a["category"] == cat)
    html_content += f'    <button class="tab-btn" onclick="filterCategory(\'{cat}\')">{cat.upper()} ({cat_count})</button>\n'

html_content += """  </div>
</header>

<div class="section-title">Cinematic Showcase &amp; Environment Inspection</div>
<div class="gallery-grid">
  <div class="gallery-card">
    <video controls autoplay loop muted poster="../showcase/01_establishing_wide.png">
      <source src="../showcase/showcase_walkthrough.mp4" type="video/mp4">
    </video>
    <div class="gallery-info">
      <h3>Cinematic Walkthrough (MP4)</h3>
      <p>Dynamic camera traveling from the airlock blast door along the mezzanine catwalk past the monitoring console and down into the geothermal reactor hall.</p>
    </div>
  </div>

  <div class="gallery-card">
    <img src="../showcase/01_establishing_wide.png" alt="Establishing Wide View">
    <div class="gallery-info">
      <h3>01 — Establishing Wide Angle (1920x1080)</h3>
      <p>Full view of the 12m x 16m double-height facility showing structural column rhythm, mezzanine catwalk, and central reactor core.</p>
    </div>
  </div>

  <div class="gallery-card">
    <img src="../showcase/02_architectural_scale.png" alt="Architectural Scale">
    <div class="gallery-info">
      <h3>02 — Architectural Scale (1920x1080)</h3>
      <p>Low-angle perspective emphasizing monolithic brutalist concrete piers, overhead I-beams, and 4m vertical module transitions.</p>
    </div>
  </div>

  <div class="gallery-card">
    <img src="../showcase/03_material_detail.png" alt="Material Detail">
    <div class="gallery-info">
      <h3>03 — Material &amp; Detail Close-Up (1920x1080)</h3>
      <p>Focus on retro-industrial telemetry console, workbench vise, wall-mounted electrical junction box, and board-formed concrete aggregate.</p>
    </div>
  </div>

  <div class="gallery-card">
    <img src="../showcase/04_hero_core_focus.png" alt="Hero Core Focus">
    <div class="gallery-info">
      <h3>04 — Hero Geothermal Compression Reactor (1920x1080)</h3>
      <p>Centerpiece focal asset featuring glowing cyan plasma containment window, hydraulic stabilizer pistons, manifold feeder pipes, and amber beacon.</p>
    </div>
  </div>

  <div class="gallery-card">
    <img src="../showcase/showcase_360_panorama.png" alt="360 Panorama">
    <div class="gallery-info">
      <h3>05 — 360° Equirectangular Panoramic VR Inspection (2048x1024)</h3>
      <p>Spherical panoramic capture from the mezzanine catwalk center for VR head-mounted displays and spatial inspection.</p>
    </div>
  </div>
</div>

<div class="section-title">Modular Asset Catalog ({len(assets)} Production GLB Models)</div>
<div class="asset-grid" id="assetGrid">
"""

for a in assets:
    dims = f"{a['dimensions_m'][0]} × {a['dimensions_m'][1]} × {a['dimensions_m'][2]} m"
    mats = ", ".join(a["materials"])
    html_content += f"""  <div class="asset-card" data-category="{a['category']}">
    <img class="asset-thumb" src="thumbnails/{a['name']}.png" alt="{a['name']}">
    <div class="asset-body">
      <span class="badge">{a['category']}</span>
      <div class="asset-name">{a['name']}</div>
      <table class="specs-table">
        <tr><td>Dimensions</td><td>{dims}</td></tr>
        <tr><td>Geometry</td><td>{a['polygons']} Quads / {a['vertices']} Verts</td></tr>
        <tr><td>Materials</td><td>{mats}</td></tr>
      </table>
      <a class="download-btn" href="../../{a['rel_path']}" download>Download GLB ({a['filename']})</a>
    </div>
  </div>
"""

html_content += """</div>

<script>
function filterCategory(cat) {
  const cards = document.querySelectorAll('.asset-card');
  const buttons = document.querySelectorAll('.tab-btn');
  buttons.forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  
  cards.forEach(c => {
    if (cat === 'all' || c.getAttribute('data-category') === cat) {
      c.style.display = 'block';
    } else {
      c.style.display = 'none';
    }
  });
}
</script>

</body>
</html>
"""

with open(HTML_OUTPUT, "w") as f:
    f.write(html_content)
print(f"Generated standalone HTML catalog viewer: {HTML_OUTPUT}")
