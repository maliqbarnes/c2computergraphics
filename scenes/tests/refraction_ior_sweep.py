"""Refraction demo: refraction_ior_sweep."""
from ray import *
from utils import vec
from glass import Glass
from scenes.checker import CheckerPlane

NAME = "refraction_ior_sweep"
DESCRIPTION = ("Four spheres with the same size and position, changing only the index of "
               "refraction: 1.0 (air), 1.33 (water), 1.5 (glass), 2.4 (diamond), left to right. "
               "At 1.0 the sphere is basically invisible since nothing bends; as the IOR goes up "
               "the checkerboard inside bends more and the edges reflect more.")


def build_scene():
    # same sphere 4 times, only the ior changes
    white = Material(vec([0.8, 0.8, 0.8]))
    dark = Material(vec([0.1, 0.1, 0.1]))
    iors = [1.0, 1.33, 1.5, 2.4]
    objects = [
      Sphere(vec([-1.5 + i, -0.1, 0]), 0.4, Glass(ior)) for i, ior in enumerate(iors)
    ]

    scene = Scene(objects + [CheckerPlane(-0.5, 0.2, white, dark)])
    lights = [PointLight(vec([12, 10, 5]), vec([300, 300, 300])), AmbientLight(0.1)]
    camera = Camera(vec([0, 1.2, 6]), target=vec([0, -0.1, 0]), vfov=25, aspect=16 / 9)
    return camera, scene, lights
