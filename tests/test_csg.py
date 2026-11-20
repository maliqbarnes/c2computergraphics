"""Checks for csg.py. Run: python tests/test_csg.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np

from ray import Material, Ray, Sphere
from utils import vec
from csg import CSG, HalfSpace, combine, sphere_intervals

M = Material(vec([0.5, 0.5, 0.5]))
A = Sphere(vec([-0.5, 0, 0]), 1.0, M)
B = Sphere(vec([0.5, 0, 0]), 1.0, M)
RAY_X = Ray(vec([-5, 0, 0]), vec([1, 0, 0]))  # along x through both centers


def ts(iv):
    return [(round(i[0], 4), round(i[2], 4)) for i in iv]


def test_sphere_intervals():
    assert ts(sphere_intervals(A, RAY_X)) == [(3.5, 5.5)]
    assert sphere_intervals(A, Ray(vec([-5, 5, 0]), vec([1, 0, 0]))) == []


def test_ops():
    a, b = sphere_intervals(A, RAY_X), sphere_intervals(B, RAY_X)
    assert ts(combine("union", a, b)) == [(3.5, 6.5)]
    assert ts(combine("intersection", a, b)) == [(4.5, 5.5)]
    assert ts(combine("difference", a, b)) == [(3.5, 4.5)]


def test_difference_normal_flipped():
    # B-A: ray travels +x, A=[−0.5..+0.5], B=[−0.5..+1.5] roughly.
    # First hit of B-A is at A's exit (t≈5.5). A's outward normal there
    # is [+1,0,0] (pointing away from A's center at -0.5).
    # For a difference we're looking at A's *inside*, so normal flips to [-1,0,0].
    hit = CSG("difference", B, A).intersect(RAY_X)
    assert abs(hit.t - 5.5) < 1e-4
    assert np.allclose(hit.normal, [-1, 0, 0], atol=1e-4)  # inside of A, flipped outward


def test_miss_and_halfspace():
    assert CSG("intersection", A, B).intersect(Ray(vec([-5, 5, 0]), vec([1, 0, 0]))).t == np.inf
    cut = CSG("difference", A, HalfSpace(vec([-0.5, 0, 0]), vec([-1, 0, 0]), M))
    assert abs(cut.intersect(RAY_X).t - 4.5) < 1e-4


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
