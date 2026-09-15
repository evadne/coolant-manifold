"""Viewport defaults for the millimetre-scale rack scene; no geometry changes."""
import bpy
from mathutils import Vector


def configure_context_viewports(scene, frame=True, target=(0, 180, 625), distance=3000, clean=False):
    target = Vector(target)
    rotation = (scene.camera.location - target).to_track_quat('Z', 'Y')
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type != 'VIEW_3D':
                    continue
                # 0.01 mm near clip destroys depth precision at rack-scale distances.
                space.clip_start = 5.0
                space.clip_end = 10000.0
                if clean:
                    space.overlay.show_extras = False
                    space.overlay.show_floor = False
                    space.overlay.show_axis_x = False
                    space.overlay.show_axis_y = False
                    space.shading.color_type = 'MATERIAL'
                if frame:
                    space.lens = 35
                    view = space.region_3d
                    view.view_location = target
                    view.view_rotation = rotation
                    view.view_distance = distance
                    view.view_perspective = 'PERSP'
