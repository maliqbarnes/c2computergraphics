"""Refraction demo: refraction_checkerboard."""
from ray import *
from utils import vec
from glass import Glass
from scenes.checker import CheckerPlane

NAME = "refraction_checkerboard"
DESCRIPTION = ("A clear glass sphere (IOR 1.5) resting on a checkerboard. Through the sphere the "
               "squares look flipped upside down and shrunk, like a lens, because rays bend "
               "entering and leaving the glass (Snell's law). The edge of the sphere picks up "
               "faint reflections from Fresnel.")


def build_scene():
    # a checkerboard behind/under the glass makes the bending easy to see
    white = Material(vec([0.8, 0.8, 0.8]))
    dark = Material(vec([0.1, 0.1, 0.1]))
    objects = [
      Sphere(vec([0, 0, 0]), 0.5, Glass(1.5)),
    ]

    scene = Scene(objects + [CheckerPlane(-0.5, 0.25, white, dark)])
    lights = [PointLight(vec([12, 10, 5]), vec([300, 300, 300])), AmbientLight(0.1)]
    camera = Camera(vec([3, 1.7, 5]), target=vec([0, 0, 0]), vfov=25, aspect=16 / 9)
    return camera, scene, lights
