"""Refraction demo: fresnel_angle."""
from ray import *
from utils import vec
from glass import Glass
from scenes.checker import CheckerPlane

NAME = "fresnel_angle"
DESCRIPTION = ("Fresnel vs. viewing angle, like looking across a lake. A flat sheet of water "
               "(IOR 1.33) covers a checkerboard. Near the camera we look down steeply, so most "
               "light passes through and the checkerboard shows. Farther away we look at a "
               "grazing angle, so Schlick's reflectance goes toward 1 and the surface turns into "
               "a mirror for the sky and the colored balls.")


def build_scene():
    # the "water" is a huge sphere so its top is basically flat; the checkerboard sits under it
    # (more ambient here bc the water blocks the point light's shadow rays to the floor)
    white = Material(vec([0.8, 0.8, 0.8]))
    dark = Material(vec([0.1, 0.1, 0.1]))
    objects = [
      Sphere(vec([0, -3000.5, 0]), 3000, Glass(1.33, tint=(0.85, 0.95, 1.0))),
      Sphere(vec([-1.2, -0.1, -3]), 0.4, Material(vec([0.9, 0.2, 0.2]), 0.3)),
      Sphere(vec([0.2, -0.1, -4.5]), 0.4, Material(vec([0.9, 0.8, 0.1]), 0.3)),
      Sphere(vec([1.6, -0.1, -3.5]), 0.4, Material(vec([0.2, 0.5, 0.9]), 0.3)),
    ]

    scene = Scene(objects + [CheckerPlane(-0.8, 0.4, white, dark, extent=15)],
                  bg_color=vec([0.45, 0.6, 0.85]))
    lights = [PointLight(vec([6, 10, 5]), vec([300, 300, 300])), AmbientLight(0.35)]
    camera = Camera(vec([0, 0.1, 4]), target=vec([0, -0.5, -2]), vfov=45, aspect=16 / 9)
    return camera, scene, lights
