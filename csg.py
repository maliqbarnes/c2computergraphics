"""Constructive solid geometry built on A4's Sphere. Owner: Person A

A CSG object goes in Scene(surfs) like any other surface: it only needs
intersect(ray) -> Hit. Internally, children report every interval where
the ray is inside them, as a list of (t_in, hit_in, t_out, hit_out).

Things to know about our ray.py:
- Sphere.intersect already has the quadratic; sphere_intervals needs both
  roots (t0, t1), not just the nearest one.
- Ray directions are not unit length; that's fine for t, but normalize
  normals.
- Shadow rays and reflection rays call Scene.intersect -> CSG.intersect, so
  respect ray.start / ray.end there or you'll get self-shadowing.
"""
import numpy as np

from ray import Hit, Sphere, no_hit


def sphere_intervals(sphere, ray):
    # TODO(A): solve the ray-sphere quadratic (same math as A4 Sphere.intersect)
    # and return [(t0, Hit0, t1, Hit1)] with outward normals, or [] on a miss.
    raise NotImplementedError


class HalfSpace:
    """Everything behind a plane through `point` with outward `normal`."""

    def __init__(self, point, normal, material):
        self.point, self.normal, self.material = point, normal, material


def halfspace_intervals(plane, ray):
    # TODO(A): one interval: (-inf, plane hit) or (plane hit, inf) depending on
    # the side the ray starts on; [] or (-inf, inf) if parallel.
    # Two half-spaces intersected = the Pac-Man mouth wedge.
    raise NotImplementedError


def intervals(surf, ray):
    if isinstance(surf, Sphere):
        return sphere_intervals(surf, ray)
    if isinstance(surf, HalfSpace):
        return halfspace_intervals(surf, ray)
    if isinstance(surf, CSG):
        return surf.intervals(ray)
    raise TypeError(f"CSG does not support {type(surf).__name__}")


def combine(op, a, b):
    # TODO(A): merge two sorted interval lists for "union", "intersection",
    # or "difference". For difference, intervals that come from b must have
    # their normals flipped.
    raise NotImplementedError


class CSG:
    def __init__(self, op, left, right, material=None):
        assert op in ("union", "intersection", "difference")
        self.op, self.left, self.right = op, left, right
        self.material = material  # if set, overrides child materials

    def intervals(self, ray):
        return combine(self.op, intervals(self.left, ray), intervals(self.right, ray))

    def intersect(self, ray):
        # TODO(A): return the first entry Hit with ray.start <= t <= ray.end
        # (set hit.material = self.material if given), else no_hit.
        raise NotImplementedError
