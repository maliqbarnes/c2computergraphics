"""Refraction demo: refraction_tir."""
from ray import *
from utils import vec
from glass import Glass, refract
from scenes.checker import CheckerPlane

NAME = "refraction_tir"
DESCRIPTION = ("Total internal reflection. Left: a glass sphere (IOR 1.5) with an air bubble "
               "inside (relative IOR 1/1.5). Light inside the glass hitting the bubble at a steep "
               "angle can't get out, so the bubble's rim turns into a mirror. Right: the same "
               "sphere colored green wherever a ray hit total internal reflection, to show exactly "
               "where it happens.")


class TIRDebugGlass(Glass):
    """Same as Glass, but paints any ray that hits total internal reflection solid green."""

    def shade(self, ray, hit, scene, lights, depth, shade_fn, max_depth):
        # check the same entering/exiting rule as Glass.shade, then ask refract for TIR
        d = ray.direction / np.linalg.norm(ray.direction)
        n = hit.normal
        if np.dot(d, n) < 0:
          n1, n2 = 1.0, self.ior
        else:
          n = -n
          n1, n2 = self.ior, 1.0
        if depth < max_depth and refract(d, n, n1, n2) is None:
          return vec([0.0, 1.0, 0.0])
        return super().shade(ray, hit, scene, lights, depth, shade_fn, max_depth)


def build_scene():
    # a sphere can't have TIR by itself (light always gets back out), so put an air bubble
    # inside: going from glass into air is what can go past the critical angle
    white = Material(vec([0.8, 0.8, 0.8]))
    dark = Material(vec([0.1, 0.1, 0.1]))
    objects = [
      Sphere(vec([-0.7, 0.1, 0]), 0.6, Glass(1.5)),
      Sphere(vec([-0.7, 0.1, 0]), 0.35, Glass(1 / 1.5)),
      Sphere(vec([0.7, 0.1, 0]), 0.6, TIRDebugGlass(1.5)),
      Sphere(vec([0.7, 0.1, 0]), 0.35, TIRDebugGlass(1 / 1.5)),
    ]

    scene = Scene(objects + [CheckerPlane(-0.5, 0.2, white, dark)])
    lights = [PointLight(vec([12, 10, 5]), vec([300, 300, 300])), AmbientLight(0.1)]
    camera = Camera(vec([0, 1.2, 6]), target=vec([0, 0.05, 0]), vfov=22, aspect=16 / 9)
    return camera, scene, lights
