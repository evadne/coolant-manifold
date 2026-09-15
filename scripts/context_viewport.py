"""Viewport defaults for the millimetre-scale 24U scene; no geometry changes."""
import bpy
from mathutils import Vector


def configure_context_viewports(scene, frame=True):
    target = Vector((0, 180, 625))
    rotation = (scene.camera.location - target).to_track_quat('Z', 'Y')
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type != 'VIEW_3D':
                    continue
                # 0.01 mm near clip destroys depth precision at rack-scale distances.
                space.clip_start = 5.0
                space.clip_end = 10000.0
                if frame:
                    space.lens = 35
                    view = space.region_3d
                    view.view_location = target
                    view.view_rotation = rotation
                    view.view_distance = 3000
                    view.view_perspective = 'PERSP'
