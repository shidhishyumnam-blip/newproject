"""
Blender-based 3D scene renderer.

Run this file using Blender's Python environment.
"""

import bpy
import math
from mathutils import Vector

from engine.environments import get_environment


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def material(name, color, roughness=0.8):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.roughness = roughness
    return mat


def cube(name, location, scale, mat):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=location
    )
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True
    )
    obj.data.materials.append(mat)
    return obj


def cylinder(name, location, radius, depth, mat):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=radius,
        depth=depth,
        location=location
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def setup_camera():
    bpy.ops.object.camera_add(
        location=(8, -12, 8)
    )

    camera = bpy.context.object
    camera.rotation_euler = (
        Vector((0, 0, 2)) - camera.location
    ).to_track_quat("-Z", "Y").to_euler()

    camera.data.lens = 40
    bpy.context.scene.camera = camera


def setup_lighting():
    bpy.ops.object.light_add(
        type="AREA",
        location=(0, -5, 9)
    )

    light = bpy.context.object
    light.data.energy = 1600
    light.data.shape = "DISK"
    light.data.size = 8


def build_ship_deck():
    wood = material("Weathered wood", (0.20, 0.12, 0.07))
    dark = material("Dark timber", (0.09, 0.055, 0.035))

    cube("Ship deck", (0, 0, 0), (14, 10, 0.3), wood)

    for x in range(-6, 7, 2):
        cube("Deck plank", (x, 0, 0.17), (0.08, 10, 0.04), dark)

    cube("Main mast", (0, 2, 3), (0.35, 0.35, 6), dark)

    for x in (-4, 4):
        cylinder(
            "Cargo barrel",
            (x, 1, 0.9),
            0.55,
            1.4,
            dark
        )


def build_cabin():
    wood = material("Cabin wood", (0.18, 0.095, 0.045))

    cube("Cabin floor", (0, 0, 0), (9, 8, 0.3), wood)

    for x in (-4.3, 4.3):
        cube("Cabin wall", (x, 0, 2), (0.3, 8, 4), wood)

    cube("Back wall", (0, 4, 2), (9, 0.3, 4), wood)

    cube("Captain desk", (0, 1, 1), (3, 1.2, 0.3), wood)

    cube("Chair seat", (0, -1, 0.8), (1, 1, 0.2), wood)


def build_environment(name):
    environment = get_environment(name)

    clear_scene()

    if name == "ship_deck":
        build_ship_deck()
    elif name == "captain_cabin":
        build_cabin()
    else:
        ground = material(
            "Environment ground",
            (0.12, 0.16, 0.19)
        )
        cube(
            environment["name"],
            (0, 0, -0.3),
            (14, 10, 0.5),
            ground
        )

    setup_camera()
    setup_lighting()

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 50

    scene.world.color = (0.12, 0.12, 0.12)

    return scene


def render_scene(name, output_path):
    scene = build_environment(name)
    scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    render_scene(
        "ship_deck",
        "preview.png"
  )
  
