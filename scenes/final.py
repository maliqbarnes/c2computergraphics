"""Final Pac-Man still image.

    python scenes/final.py --nx 960
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ray import *
from utils import vec
from cli import render
from csg import CSG, HalfSpace
from glass import Glass


def build_scene():
    objects = []
    # TODO: dark floor
    # TODO(A): Pac-Man = CSG("difference", Sphere, CSG("intersection", HalfSpace, HalfSpace))
    # TODO: row of pellet spheres
    # TODO(B): ghosts / power pellets with Glass material

    scene = Scene(objects, bg_color=vec([0.0, 0.0, 0.02]))
    # TODO: 2-3 colored lights
    lights = [PointLight(vec([12, 10, 5]), vec([300, 300, 300])), AmbientLight(0.1)]
    camera = Camera(vec([3, 1.7, 5]), target=vec([0, 0, 0]), vfov=25, aspect=16 / 9)
    return camera, scene, lights


if __name__ == "__main__":
    render(*build_scene())
