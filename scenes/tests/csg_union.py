"""CSG demo: union.

Shows that two overlapping spheres combine into one merged blob.
The seam where they overlap disappears; only the outer surface is visible.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ray import *
from utils import vec
from csg import CSG

NAME = "csg_union"
DESCRIPTION = "Union of two overlapping spheres: the merge operation."


def build_scene():
    gray = Material(vec([0.2, 0.2, 0.2]), k_m=0.3)
    red  = Material(vec([0.8, 0.2, 0.2]), k_s=0.4, p=60)
    blue = Material(vec([0.2, 0.2, 0.8]), k_s=0.4, p=60)

    left  = Sphere(vec([-0.35, 0, 0]), 0.5, red)
    right = Sphere(vec([ 0.35, 0, 0]), 0.5, blue)
    merged = CSG("union", left, right)

    scene = Scene([
        merged,
        Sphere(vec([0, -40, 0]), 39.5, gray),
    ])
    lights = [
        PointLight(vec([12, 10, 5]), vec([300, 300, 300])),
        AmbientLight(0.1),
    ]
    camera = Camera(vec([3, 1.7, 5]), target=vec([0, 0, 0]), vfov=25, aspect=16/9)
    return camera, scene, lights
