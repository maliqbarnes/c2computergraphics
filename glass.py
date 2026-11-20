"""Refraction and Fresnel. Owner: Person B

Glass is used as a surface's material, e.g. Sphere(c, r, Glass(1.5)).
ray.shade() needs one hook so it calls Glass.shade instead of Phong;
see the TODO(B) at the top of ray.shade.
"""
import numpy as np

from ray import Ray


def reflect(d, n):
    # TODO(B): mirror direction of d about unit normal n
    raise NotImplementedError


def refract(d, n, n1, n2):
    # TODO(B): Snell's law for unit d, unit n facing against d.
    # Return the refracted direction, or None on total internal reflection.
    raise NotImplementedError


def fresnel_schlick(cos_theta, n1, n2):
    # TODO(B): Schlick approximation of reflectance in [0, 1]
    raise NotImplementedError


class Glass:
    def __init__(self, ior=1.5, tint=(1.0, 1.0, 1.0)):
        self.ior = ior
        self.tint = np.array(tint, np.float32)

    def shade(self, ray, hit, scene, lights, depth, shade_fn, max_depth):
        # TODO(B):
        #  1. entering if dot(ray dir, hit.normal) < 0, else flip n and swap n1/n2
        #  2. reflected and refracted rays (offset origins to avoid acne)
        #  3. trace each with scene.intersect + shade_fn(..., depth + 1),
        #     returning black once depth >= max_depth
        #  4. blend with fresnel_schlick (all reflection on TIR), multiply by tint
        raise NotImplementedError
