"""Checks for glass.py. Run: python tests/test_glass.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np

from glass import fresnel_schlick, reflect, refract

N = np.array([0.0, 1.0, 0.0])


def test_reflect():
    d = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)
    assert np.allclose(reflect(d, N), [d[0], -d[1], 0])


def test_refract_straight_and_snell():
    assert np.allclose(refract(np.array([0.0, -1.0, 0.0]), N, 1.0, 1.5), [0, -1, 0])
    d = np.array([np.sin(0.5), -np.cos(0.5), 0.0])
    t = refract(d, N, 1.0, 1.5)
    assert abs(np.linalg.norm(t) - 1) < 1e-6
    assert abs(1.0 * np.sin(0.5) - 1.5 * t[0]) < 1e-6


def test_total_internal_reflection():
    d = np.array([np.sin(1.2), -np.cos(1.2), 0.0])
    assert refract(d, N, 1.5, 1.0) is None


def test_fresnel():
    assert abs(fresnel_schlick(1.0, 1.0, 1.5) - 0.04) < 1e-6
    assert abs(fresnel_schlick(0.0, 1.0, 1.5) - 1.0) < 1e-6


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
