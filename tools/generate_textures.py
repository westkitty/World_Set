import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TEXTURE_DIR = "/Users/andrew/World_Set/textures"
os.makedirs(TEXTURE_DIR, exist_ok=True)

def generate_noise(width, height, octaves=4, base_scale=32):
    """Generate simple multi-octave value noise."""
    random.seed(42)
    grid = [[random.random() for _ in range(height)] for _ in range(width)]
    # Simple smooth box filter approximations
    img = Image.new("L", (width, height))
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            val = 0
            weight_sum = 0
            w = 1.0
            scale = base_scale
            for o in range(octaves):
                gx = (x // scale) % (width // scale + 1)
                gy = (y // scale) % (height // scale + 1)
                val += random.random() * w
                weight_sum += w
                w *= 0.5
                scale = max(2, scale // 2)
            v_int = int((val / weight_sum) * 255)
            pixels[x, y] = max(0, min(255, v_int))
    return img.filter(ImageFilter.GaussianBlur(radius=1.5))

def generate_normal_from_height(height_img, strength=2.0):
    """Generate a tangent space normal map (RGB) from a heightmap."""
    w, h = height_img.size
    h_pixels = height_img.load()
    normal_img = Image.new("RGB", (w, h))
    n_pixels = normal_img.load()
    
    for y in range(h):
        for x in range(w):
            x_prev = (x - 1) % w
            x_next = (x + 1) % w
            y_prev = (y - 1) % h
            y_next = (y + 1) % h
            
            dx = (h_pixels[x_next, y] - h_pixels[x_prev, y]) / 255.0 * strength
            dy = (h_pixels[x, y_next] - h_pixels[x, y_prev]) / 255.0 * strength
            
            # Normal vector (-dx, -dy, 1.0) normalized
            nz = 1.0
            length = math.sqrt(dx*dx + dy*dy + nz*nz)
            nx = -dx / length
            ny = -dy / length
            nz = nz / length
            
            # Convert to [0, 255]
            r = int((nx * 0.5 + 0.5) * 255)
            g = int((ny * 0.5 + 0.5) * 255)
            b = int((nz * 0.5 + 0.5) * 255)
            n_pixels[x, y] = (r, g, b)
    return normal_img

print("Generating Concrete textures...")
# 1. Concrete (1024x1024)
w, h = 1024, 1024
concrete_albedo = Image.new("RGB", (w, h), (85, 90, 93))
draw = ImageDraw.Draw(concrete_albedo)
noise = generate_noise(w, h, octaves=4, base_scale=64)
noise_pixels = noise.load()
c_pixels = concrete_albedo.load()

height_map = Image.new("L", (w, h))
h_pixels = height_map.load()

for x in range(w):
    for y in range(h):
        n = (noise_pixels[x, y] - 128) / 128.0
        # Horizontal board-form striations
        band = math.sin(y * 0.05) * 8
        r = int(max(0, min(255, 88 + n * 24 + band)))
        g = int(max(0, min(255, 92 + n * 24 + band)))
        b = int(max(0, min(255, 95 + n * 22 + band)))
        c_pixels[x, y] = (r, g, b)
        h_pixels[x, y] = int(max(0, min(255, 128 + n * 40 + band * 2)))

concrete_albedo.save(os.path.join(TEXTURE_DIR, "tex_concrete_albedo.png"))
concrete_rough = noise.point(lambda p: int(190 + (p - 128) * 0.3))
concrete_rough.save(os.path.join(TEXTURE_DIR, "tex_concrete_roughness.png"))
concrete_normal = generate_normal_from_height(height_map, strength=1.5)
concrete_normal.save(os.path.join(TEXTURE_DIR, "tex_concrete_normal.png"))

print("Generating Heavy Steel textures...")
# 2. Heavy Painted Steel (1024x1024)
steel_albedo = Image.new("RGB", (w, h), (52, 60, 56)) # Industrial olive/charcoal
s_pixels = steel_albedo.load()
steel_rough = Image.new("L", (w, h), 130) # ~0.5 roughness
sr_pixels = steel_rough.load()
steel_metal = Image.new("L", (w, h), 20) # mostly painted non-metal
sm_pixels = steel_metal.load()
s_height = Image.new("L", (w, h), 128)
sh_pixels = s_height.load()

# Add panel line grooves and corner rivets
for x in range(w):
    for y in range(h):
        # Edge proximity for chipping
        edge_dist = min(x % 256, 256 - (x % 256), y % 256, 256 - (y % 256))
        n = (noise_pixels[x, y] - 128) / 128.0
        if edge_dist < 4:
            # Panel groove
            s_pixels[x, y] = (25, 28, 26)
            sr_pixels[x, y] = 200
            sm_pixels[x, y] = 50
            sh_pixels[x, y] = 60
        elif edge_dist < 10 and n > 0.3:
            # Chipped paint revealing steel
            s_pixels[x, y] = (160, 165, 170) # bare steel
            sr_pixels[x, y] = 80
            sm_pixels[x, y] = 230
            sh_pixels[x, y] = 140
        else:
            r = int(max(0, min(255, 54 + n * 12)))
            g = int(max(0, min(255, 64 + n * 14)))
            b = int(max(0, min(255, 60 + n * 12)))
            s_pixels[x, y] = (r, g, b)
            sr_pixels[x, y] = int(max(0, min(255, 130 + n * 30)))
            sm_pixels[x, y] = 20
            sh_pixels[x, y] = 128

steel_albedo.save(os.path.join(TEXTURE_DIR, "tex_steel_albedo.png"))
steel_rough.save(os.path.join(TEXTURE_DIR, "tex_steel_roughness.png"))
steel_metal.save(os.path.join(TEXTURE_DIR, "tex_steel_metallic.png"))
steel_normal = generate_normal_from_height(s_height, strength=2.2)
steel_normal.save(os.path.join(TEXTURE_DIR, "tex_steel_normal.png"))

print("Generating Industrial Grate textures...")
# 3. Galvanized Floor Grate (512x512)
gw, gh = 512, 512
grate_albedo = Image.new("RGB", (gw, gh), (110, 115, 120))
grate_rough = Image.new("L", (gw, gh), 110)
grate_metal = Image.new("L", (gw, gh), 230)
grate_height = Image.new("L", (gw, gh), 128)
ga_pixels = grate_albedo.load()
gr_pixels = grate_rough.load()
gm_pixels = grate_metal.load()
gh_pixels = grate_height.load()

cell_size = 32
for x in range(gw):
    for y in range(gh):
        cx = x % cell_size
        cy = y % cell_size
        # Diamond grate slot
        dx = abs(cx - cell_size/2) / (cell_size/2)
        dy = abs(cy - cell_size/2) / (cell_size/2)
        if (dx + dy) < 0.65:
            # Perforation hole / recessed depth
            ga_pixels[x, y] = (18, 20, 22)
            gr_pixels[x, y] = 230
            gm_pixels[x, y] = 20
            gh_pixels[x, y] = 30
        else:
            # Metal rib
            edge = 1.0 - (dx + dy)
            ga_pixels[x, y] = (115, 120, 125)
            gr_pixels[x, y] = 100
            gm_pixels[x, y] = 230
            gh_pixels[x, y] = 210

grate_albedo.save(os.path.join(TEXTURE_DIR, "tex_grate_albedo.png"))
grate_rough.save(os.path.join(TEXTURE_DIR, "tex_grate_roughness.png"))
grate_metal.save(os.path.join(TEXTURE_DIR, "tex_grate_metallic.png"))
grate_normal = generate_normal_from_height(grate_height, strength=3.0)
grate_normal.save(os.path.join(TEXTURE_DIR, "tex_grate_normal.png"))

print("Generating Hazard Stripe textures...")
# 4. Hazard Stripes (512x512)
hz_albedo = Image.new("RGB", (512, 512))
hz_draw = ImageDraw.Draw(hz_albedo)
hz_rough = Image.new("L", (512, 512), 160)
for i in range(-512, 1024, 64):
    hz_draw.polygon([(i, 0), (i+32, 0), (i+32+512, 512), (i+512, 512)], fill=(245, 183, 0)) # Yellow
    hz_draw.polygon([(i+32, 0), (i+64, 0), (i+64+512, 512), (i+32+512, 512)], fill=(28, 28, 30)) # Charcoal Black
# Add scuffing
hz_albedo = hz_albedo.filter(ImageFilter.SMOOTH_MORE)
hz_albedo.save(os.path.join(TEXTURE_DIR, "tex_hazard_albedo.png"))
hz_rough.save(os.path.join(TEXTURE_DIR, "tex_hazard_roughness.png"))

print("Generating Diagnostic Display textures...")
# 5. Diagnostic Screen UI (512x512)
screen = Image.new("RGB", (512, 512), (10, 22, 28))
sdraw = ImageDraw.Draw(screen)
# Grid lines
for y in range(0, 512, 32):
    sdraw.line([(0, y), (512, y)], fill=(18, 48, 55), width=1)
for x in range(0, 512, 32):
    sdraw.line([(x, 0), (x, 512)], fill=(18, 48, 55), width=1)

# Waveforms & bargraphs
points = []
for x in range(30, 480, 4):
    y = 200 + math.sin(x * 0.08) * 45 + math.cos(x * 0.02) * 20
    points.append((x, int(y)))
sdraw.line(points, fill=(27, 231, 255), width=3) # Cyan phosphor waveform

# Header & diagnostic readout bars
sdraw.rectangle([(30, 30), (480, 70)], outline=(27, 231, 255), width=2)
sdraw.rectangle([(40, 40), (280, 60)], fill=(27, 231, 255))
sdraw.rectangle([(30, 90), (480, 110)], outline=(255, 159, 28), width=1)
sdraw.rectangle([(35, 93), (380, 107)], fill=(255, 159, 28)) # Amber load

# Pressure gauges / bars
for i in range(6):
    bx = 40 + i * 75
    h_bar = int(100 + math.sin(i * 1.5) * 60)
    sdraw.rectangle([(bx, 440 - h_bar), (bx + 50, 440)], fill=(27, 231, 255) if i < 4 else (255, 159, 28))
    sdraw.rectangle([(bx, 280), (bx + 50, 440)], outline=(30, 80, 90), width=1)

screen.save(os.path.join(TEXTURE_DIR, "tex_screen_cyan.png"))

print("Generating Signage textures...")
# 6. Sector Sign (1024x512)
sign = Image.new("RGB", (1024, 512), (32, 36, 40))
signdraw = ImageDraw.Draw(sign)
# Border frame
signdraw.rectangle([(16, 16), (1008, 496)], outline=(245, 183, 0), width=8)
# Warning stripes top and bottom
for i in range(24, 1000, 40):
    signdraw.polygon([(i, 24), (i+20, 24), (i+30, 60), (i+10, 60)], fill=(245, 183, 0))
    signdraw.polygon([(i, 452), (i+20, 452), (i+30, 488), (i+10, 488)], fill=(245, 183, 0))

# Bold text simulation
# Sector 04 header bar
signdraw.rectangle([(60, 90), (964, 190)], fill=(245, 183, 0))
# Inner dark banner
signdraw.rectangle([(70, 100), (954, 180)], fill=(24, 26, 28))
# Draw stylized glyphs / lettering
# "SECTOR 04"
signdraw.rectangle([(100, 120), (320, 160)], fill=(245, 183, 0))
signdraw.rectangle([(360, 120), (700, 160)], fill=(255, 255, 255))
signdraw.rectangle([(740, 120), (920, 160)], fill=(27, 231, 255))

# Sub-aquifer descriptions
signdraw.rectangle([(60, 220), (500, 250)], fill=(200, 205, 210))
signdraw.rectangle([(60, 270), (780, 295)], fill=(150, 155, 160))
signdraw.rectangle([(60, 315), (650, 340)], fill=(150, 155, 160))
signdraw.rectangle([(60, 360), (420, 385)], fill=(245, 183, 0))

# Directional chevron arrows
for c in range(3):
    cx = 850 + c * 35
    signdraw.polygon([(cx, 300), (cx+25, 330), (cx, 360), (cx-10, 360), (cx+15, 330), (cx-10, 300)], fill=(245, 183, 0))

sign.save(os.path.join(TEXTURE_DIR, "tex_sign_sector.png"))

# 7. Hazard Triangle Sign (512x512)
haz = Image.new("RGB", (512, 512), (35, 38, 42))
hazdraw = ImageDraw.Draw(haz)
hazdraw.polygon([(256, 40), (480, 440), (32, 440)], fill=(245, 183, 0))
hazdraw.polygon([(256, 80), (445, 420), (67, 420)], fill=(24, 26, 28))
# Inner warning exclamation / biohazard motif
hazdraw.polygon([(256, 120), (420, 400), (92, 400)], fill=(245, 183, 0))
hazdraw.polygon([(256, 150), (400, 385), (112, 385)], fill=(24, 26, 28))
hazdraw.rectangle([(242, 190), (270, 300)], fill=(245, 183, 0))
hazdraw.ellipse([(240, 325), (272, 357)], fill=(245, 183, 0))
haz.save(os.path.join(TEXTURE_DIR, "tex_sign_hazard.png"))

print("All PBR textures generated successfully!")
