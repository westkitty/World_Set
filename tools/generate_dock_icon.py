#!/usr/bin/env python3
"""
Generate macOS AppIcon.icns for World Set desktop application wrapper.
Uses renders/showcase/05_stargate_portal_chamber.png as the base artwork,
applies standard Apple macOS squircle curvature, metallic cyan/slate borders,
gloss highlights, and drop shadows, and compiles via iconutil.
"""

import os
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_IMAGE = os.path.join(PROJECT_ROOT, "renders", "showcase", "05_stargate_portal_chamber.png")
OUT_PNG = os.path.join(PROJECT_ROOT, "renders", "app_icon_1024.png")
OUT_ICNS = os.path.join(PROJECT_ROOT, "renders", "AppIcon.icns")
ICONSET_DIR = os.path.join(PROJECT_ROOT, "renders", "AppIcon.iconset")

def generate_master_icon():
    print(f"Loading source artwork: {SRC_IMAGE}")
    src = Image.open(SRC_IMAGE).convert("RGBA")

    # Center of mass for the glowing Stargate portal in 1920x1080
    center_x = 1004
    crop_x = center_x - 540
    crop_img = src.crop((crop_x, 0, crop_x + 1080, 1080))
    crop_img = crop_img.resize((824, 824), Image.Resampling.LANCZOS)

    # Enhance contrast and saturation for high dock visibility
    crop_img = ImageEnhance.Contrast(crop_img).enhance(1.22)
    crop_img = ImageEnhance.Color(crop_img).enhance(1.28)

    # 1. Standard Apple squircle mask (824x824, radius=185)
    mask = Image.new("L", (824, 824), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, 824, 824], radius=185, fill=255)

    rounded_content = Image.new("RGBA", (824, 824), (0, 0, 0, 0))
    rounded_content.paste(crop_img, (0, 0), mask)

    # 2. Add high-tech border / chamfer bezel
    border_layer = Image.new("RGBA", (824, 824), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border_layer)
    border_draw.rounded_rectangle([0, 0, 823, 823], radius=185, outline=(25, 35, 50, 255), width=5)
    border_draw.rounded_rectangle([4, 4, 819, 819], radius=181, outline=(27, 231, 255, 200), width=3)
    border_draw.rounded_rectangle([8, 8, 815, 815], radius=177, outline=(10, 18, 28, 140), width=2)

    # 3. Add curved glass highlight
    gloss = Image.new("RGBA", (824, 824), (0, 0, 0, 0))
    gloss_draw = ImageDraw.Draw(gloss)
    for y in range(380):
        alpha = int(40 * (1.0 - (y / 380.0)))
        gloss_draw.line([(0, y), (824, y)], fill=(255, 255, 255, alpha))
    gloss = Image.composite(gloss, Image.new("RGBA", (824, 824), (0, 0, 0, 0)), mask)

    icon_body = Image.alpha_composite(rounded_content, gloss)
    icon_body = Image.alpha_composite(icon_body, border_layer)

    # 4. Canvas with ambient drop shadow
    canvas = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    shadow_mask = Image.new("L", (1024, 1024), 0)
    s_draw = ImageDraw.Draw(shadow_mask)
    s_draw.rounded_rectangle([100, 100 + 18, 100 + 824, 100 + 18 + 824], radius=185, fill=160)
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(24))
    shadow.paste(Image.new("RGBA", (1024, 1024), (0, 0, 0, 255)), (0, 0), shadow_mask)

    canvas = Image.alpha_composite(canvas, shadow)
    canvas.paste(icon_body, (100, 100), icon_body)

    canvas.save(OUT_PNG, "PNG")
    print(f"[PASS] Master PNG generated: {OUT_PNG} ({os.path.getsize(OUT_PNG)} bytes)")
    return canvas

def compile_icns(master_img):
    os.makedirs(ICONSET_DIR, exist_ok=True)
    specs = [
        ("icon_16x16.png", 16),
        ("icon_16x16@2x.png", 32),
        ("icon_32x32.png", 32),
        ("icon_32x32@2x.png", 64),
        ("icon_128x128.png", 128),
        ("icon_128x128@2x.png", 256),
        ("icon_256x256.png", 256),
        ("icon_256x256@2x.png", 512),
        ("icon_512x512.png", 512),
        ("icon_512x512@2x.png", 1024),
    ]

    for fname, sz in specs:
        resized = master_img.resize((sz, sz), Image.Resampling.LANCZOS)
        resized.save(os.path.join(ICONSET_DIR, fname), "PNG")

    subprocess.run(["iconutil", "-c", "icns", ICONSET_DIR, "-o", OUT_ICNS], check=True)
    print(f"[PASS] ICNS bundle generated: {OUT_ICNS} ({os.path.getsize(OUT_ICNS)} bytes)")

if __name__ == "__main__":
    img = generate_master_icon()
    compile_icns(img)
