"""Render driver - stills, 360 panorama and the cinematic walkthrough."""

from __future__ import annotations

import glob
import os

import bpy

from . import cameras, dna


def _preset(scene, pr):
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = pr["samples"]
    scene.cycles.use_denoising = pr.get("denoise", True)
    scene.render.resolution_x = pr["width"]
    scene.render.resolution_y = pr["height"]
    scene.render.use_persistent_data = True


def render_stills(scene, out_dir, report):
    os.makedirs(out_dir, exist_ok=True)
    _preset(scene, dna.RENDER["stills"])
    cams = cameras.build_stills()
    for key, cam in cams.items():
        scene.camera = cam
        scene.render.image_settings.file_format = "PNG"
        scene.render.filepath = os.path.join(out_dir, f"still_{key}.png")
        bpy.ops.render.render(write_still=True)
    report.append(f"rendered {len(cams)} stills @ "
                  f"{dna.RENDER['stills']['width']}x{dna.RENDER['stills']['height']}")


def render_pano(scene, out_dir, report):
    os.makedirs(out_dir, exist_ok=True)
    _preset(scene, dna.RENDER["panorama"])
    cam = cameras.build_panorama()
    scene.camera = cam
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = os.path.join(out_dir, "environment_360.png")
    bpy.ops.render.render(write_still=True)
    report.append(f"rendered 360 panorama @ "
                  f"{dna.RENDER['panorama']['width']}x{dna.RENDER['panorama']['height']}")


def render_walkthrough(scene, out_dir, report):
    os.makedirs(out_dir, exist_ok=True)
    pr = dna.RENDER["walkthrough"]
    _preset(scene, pr)
    cam = cameras.build_walkthrough(pr["fps"], pr["seconds"])
    scene.camera = cam
    scene.render.fps = pr["fps"]
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
    scene.render.ffmpeg.gopsize = 12
    scene.render.filepath = os.path.join(out_dir, "walk_")
    bpy.ops.render.render(animation=True)
    produced = sorted(glob.glob(os.path.join(out_dir, "walk_*.mp4")))
    final = os.path.join(out_dir, "walkthrough.mp4")
    if produced and produced[0] != final:
        os.replace(produced[0], final)
    report.append(f"rendered walkthrough {pr['seconds']}s @ {pr['fps']}fps "
                  f"({pr['width']}x{pr['height']})")
