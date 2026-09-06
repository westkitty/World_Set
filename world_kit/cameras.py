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
    cams = {}
    # 1 establishing: NE corner, looking SW across channel, evaporator, stair
    c = _cam("CAM_establishing", 30); c.location = (0.9, 0.9, 2.3)
    _aim(c, (9.0, 5.5, 2.6)); cams["establishing"] = c
    # 2 architectural scale: low down the vaulted seaward row
    c = _cam("CAM_arch", 28); c.location = (10.5, 1.4, 1.3)
    _aim(c, (2.0, 1.0, 3.2)); cams["architecture"] = c
    # 3 detail: valve + pipe + crate corner
    c = _cam("CAM_detail", 45); c.location = (3.0, 3.0, 1.4)
    _aim(c, (0.7, 4.0, 0.8)); cams["detail"] = c
    # 4 modular variation: stair + platform + catwalk
    c = _cam("CAM_variation", 30); c.location = (5.4, 2.2, 2.0)
    _aim(c, (2.0, 6.0, 2.6)); cams["variation"] = c
    # 5 hero integration: evaporator with the glazed seaward wall + beacon behind
    c = _cam("CAM_hero", 35); c.location = (2.5, 1.6, 1.7)
    _aim(c, (6.0, 6.0, 4.2)); cams["hero"] = c
    # 6 storytelling: crates by the doorway, worn threshold
    c = _cam("CAM_story", 40); c.location = (8.6, 6.0, 1.5)
    _aim(c, (9.6, 7.4, 0.7)); cams["story"] = c
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
    ob.location = (6, 4, EYE)
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
    keys = [
        (1,    (6.0, 7.6, EYE), (6.0, 4.0, 1.6)),
        (int(last * 0.25), (6.0, 5.4, EYE), (6.0, 6.0, 2.6)),
        (int(last * 0.5), (7.4, 4.0, EYE), (6.0, 6.0, 2.8)),
        (int(last * 0.75), (9.5, 2.6, EYE), (6.0, 5.5, 2.4)),
        (last, (10.6, 1.4, 1.9), (3.0, 4.0, 2.2)),
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
