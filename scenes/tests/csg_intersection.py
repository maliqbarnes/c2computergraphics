"""CSG demo: intersection.

Shows the lens-shaped region shared by two overlapping spheres.
Only the overlapping volume is rendered.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ray import *
from utils import vec
from csg import CSG

NAME = "csg_intersection"
DESCRIPTION = "Intersection of two overlapping spheres: the lens region."


def build_scene():
    gray  = Material(vec([0.2, 0.2, 0.2]), k_m=0.3)
    green = Material(vec([0.2, 0.8, 0.2]), k_s=0.4, p=60)

    left  = Sphere(vec([-0.3, 0, 0]), 0.6, green)
    right = Sphere(vec([ 0.3, 0, 0]), 0.6, green)
    lens  = CSG("intersection", left, right)

    scene = Scene([
        lens,
        Sphere(vec([0, -40, 0]), 39.5, gray),
    ])
    lights = [
        PointLight(vec([12, 10, 5]), vec([300, 300, 300])),
        AmbientLight(0.1),
    ]
    camera = Camera(vec([3, 1.7, 5]), target=vec([0, 0, 0]), vfov=25, aspect=16/9)
    return camera, scene, lights
