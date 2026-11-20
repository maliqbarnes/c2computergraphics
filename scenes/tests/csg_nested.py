"""CSG demo: nested tree.

A nested CSG: (A union B) difference C.
Shows that CSG trees of arbitrary depth work correctly.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ray import *
from utils import vec
from csg import CSG

NAME = "csg_nested"
DESCRIPTION = (
    "Nested CSG: (sphere_A union sphere_B) difference sphere_C. "
    "Demonstrates that combining CSG nodes recursively works."
)


def build_scene():
    gray   = Material(vec([0.2, 0.2, 0.2]), k_m=0.3)
    red    = Material(vec([0.8, 0.2, 0.2]), k_s=0.4, p=60)
    blue   = Material(vec([0.2, 0.2, 0.8]), k_s=0.4, p=60)
    white  = Material(vec([0.9, 0.9, 0.9]))

    A = Sphere(vec([-0.4,  0.15, 0]), 0.45, red)
    B = Sphere(vec([ 0.4,  0.15, 0]), 0.45, blue)
    C = Sphere(vec([ 0.0, -0.1,  0.3]), 0.5, white)

    combined = CSG("difference", CSG("union", A, B), C)

    scene = Scene([
        combined,
        Sphere(vec([0, -40, 0]), 39.5, gray),
    ])
    lights = [
        PointLight(vec([12, 10, 5]), vec([300, 300, 300])),
        AmbientLight(0.1),
    ]
    camera = Camera(vec([3, 1.7, 5]), target=vec([0, 0, 0]), vfov=25, aspect=16/9)
    return camera, scene, lights
