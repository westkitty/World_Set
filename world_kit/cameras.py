"""Cameras - stills, a 360 panorama and a cinematic walkthrough."""

from __future__ import annotations

import math

import bpy
from mathutils import Vector

EYE = 1.62


def _cam(name, lens=35):
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    ob = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def _aim(cam, target):
    d = Vector(target) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def _target(name):
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    e = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(e)
    return e


def build_stills() -> dict:
    """Six deliberate framings.  Positions/aims are chosen to stay clear of the
    0.95m column grid (x,y in {0,4,8,12}), the 4.44m evaporator at (6,6) and the
    spiral-stair footprint (x 0.2-3.8, y 4.2-7.8)."""
    cams = {}
    # 1 establishing: NE high corner looking SW over channel, tank, stair
    c = _cam("CAM_establishing", 28); c.location = (11.2, 7.2, 2.5)
    _aim(c, (2.5, 2.0, 1.4)); cams["establishing"] = c
    # 2 architectural scale: low down the vaulted channel row, catwalk beyond
    c = _cam("CAM_arch", 28); c.location = (1.2, 1.2, 1.5)
    _aim(c, (10.0, 2.0, 3.0)); cams["architecture"] = c
    # 3 detail: valve + pipe + crate corner (west)
    c = _cam("CAM_detail", 45); c.location = (3.0, 3.0, 1.4)
    _aim(c, (0.7, 4.0, 0.8)); cams["detail"] = c
    # 4 modular variation: spiral stair + platform + pipe (vertical circulation)
    c = _cam("CAM_variation", 30); c.location = (7.5, 3.0, 2.0)
    _aim(c, (2.0, 6.0, 3.0)); cams["variation"] = c
    # 5 hero integration: evaporator with glazed seaward wall behind
    c = _cam("CAM_hero", 32); c.location = (9.8, 6.8, 1.8)
    _aim(c, (4.5, 3.0, 2.4)); cams["hero"] = c
    # 6 storytelling: crates by the doorway, worn threshold + signage beyond
    c = _cam("CAM_story", 40); c.location = (3.4, 1.0, 1.5)
    _aim(c, (1.2, 2.6, 1.2)); cams["story"] = c
    return cams


def build_panorama():
    old = bpy.data.objects.get("CAM_pano")
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    cd = bpy.data.cameras.new("CAM_pano")
    cd.type = "PANO"
    cd.panorama_type = "EQUIRECTANGULAR"
    cd.lens = 18
    ob = bpy.data.objects.new("CAM_pano", cd)
    bpy.context.scene.collection.objects.link(ob)
    # open floor SE of the evaporator: clear of the 4m column grid, the tank
    # and the catwalk, with sightlines to tank, channel, doorway and breach
    ob.location = (8, 2.2, EYE)
    return ob


def build_walkthrough(fps, seconds):
    cam = _cam("CAM_walk", 30)
    tgt = _target("CAM_walk_target")
    con = cam.constraints.new("TRACK_TO")
    con.target = tgt
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"

    last = int(fps * seconds)
    # (frame, cam_loc, target)
    # Travels *through* the hall: enter at the NE doorway, slip down the open
    # east side (clear of the 4.44m evaporator and the column grid), then cross
    # the brine channel west to settle on the spiral stair.  Never orbits.
    keys = [
        (1,    (10.3, 7.2, EYE), (6.0, 6.0, 3.0)),
        (int(last * 0.3), (9.0, 5.2, EYE), (6.0, 6.0, 3.0)),
        (int(last * 0.55), (8.6, 3.0, EYE), (5.5, 5.0, 2.6)),
        (int(last * 0.8), (6.0, 2.0, EYE), (3.0, 4.5, 2.2)),
        (last, (3.6, 1.6, 1.9), (2.0, 5.0, 2.8)),
    ]
    for f, loc, t in keys:
        cam.location = loc
        tgt.location = t
        cam.keyframe_insert("location", frame=f)
        tgt.keyframe_insert("location", frame=f)
    # smooth
    for ob in (cam, tgt):
        if ob.animation_data and ob.animation_data.action:
            for fc in ob.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "BEZIER"
                    kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = last
    return cam
