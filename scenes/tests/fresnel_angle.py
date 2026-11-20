"""Refraction demo: fresnel_angle."""
from ray import *
from utils import vec
from glass import Glass

NAME = "fresnel_angle"
DESCRIPTION = "TODO(B): describe what this image shows."


def build_scene():
    # TODO(B): glass object(s) and a background that makes the effect visible
    objects = []

    scene = Scene(objects + [Sphere(vec([0, -40, 0]), 39.5, Material(vec([0.2, 0.2, 0.2])))])
    lights = [PointLight(vec([12, 10, 5]), vec([300, 300, 300])), AmbientLight(0.1)]
    camera = Camera(vec([3, 1.7, 5]), target=vec([0, 0, 0]), vfov=25, aspect=16 / 9)
    return camera, scene, lights
