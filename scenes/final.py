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

FLOOR_Y = -0.5


def box(lo, hi, material):
    """Axis-aligned box as the CSG intersection of 6 half-spaces."""
    lo, hi = vec(lo), vec(hi)
    faces = [
        HalfSpace(hi, vec([1, 0, 0]), material), HalfSpace(lo, vec([-1, 0, 0]), material),
        HalfSpace(hi, vec([0, 1, 0]), material), HalfSpace(lo, vec([0, -1, 0]), material),
        HalfSpace(hi, vec([0, 0, 1]), material), HalfSpace(lo, vec([0, 0, -1]), material),
    ]
    shape = faces[0]
    for f in faces[1:]:
        shape = CSG("intersection", shape, f)
    return shape


def pacman(center, radius, material):
    """Sphere minus a wedge (two half-spaces through the center) for a mouth facing +x."""
    upper = HalfSpace(center, vec([-0.5, -1, 0]), material)
    lower = HalfSpace(center, vec([-0.5, 1, 0]), material)
    return CSG("difference", Sphere(center, radius, material), CSG("intersection", upper, lower))


def ghost(center, radius, glass):
    """Glass ghost: a sphere with three scallops cut out of the bottom."""
    x, y, z = center
    r = radius
    cuts = [Sphere(vec([x + dx, y - 1.05 * r, z]), 0.36 * r, glass) for dx in (-0.55 * r, 0.0, 0.55 * r)]
    body = Sphere(vec(center), r, glass)
    for c in cuts:
        body = CSG("difference", body, c, material=glass)
    return body


def eyes(center, radius, facing):
    """Two white eyes with dark pupils on the front of a ghost, looking along `facing` (+1/-1 in x)."""
    white = Material(vec([0.9, 0.9, 0.9]), k_s=0.3, p=40)
    pupil = Material(vec([0.05, 0.05, 0.3]))
    x, y, z = center
    out = []
    for dz in (-0.35 * radius, 0.35 * radius):
        e = vec([x + facing * 0.8 * radius, y + 0.25 * radius, z + dz])
        out.append(Sphere(e, 0.22 * radius, white))
        out.append(Sphere(e + vec([facing * 0.14 * radius, 0, 0]), 0.11 * radius, pupil))
    return out


def build_scene():
    objects = []

    # dark, slightly glossy floor so the neon lights and characters reflect in it
    floor = Material(vec([0.05, 0.04, 0.12]), k_s=0.3, p=60, k_m=0.25)
    objects.append(Sphere(vec([0, FLOOR_Y - 1000, 0]), 1000, floor))

    # maze walls: two low blue boxes (CSG intersections of half-spaces) lining the corridor
    wall = Material(vec([0.05, 0.1, 0.9]), k_s=0.4, p=30)
    objects.append(box([-6, FLOOR_Y, -1.25], [3, FLOOR_Y + 0.35, -0.95], wall))
    objects.append(box([-6, FLOOR_Y, 0.95], [3, FLOOR_Y + 0.35, 1.25], wall))

    # Pac-Man (CSG sphere minus wedge) running toward +x, with an eye
    pac_c = vec([-0.6, -0.05, 0])
    pac_r = 0.45
    yellow = Material(vec([1.0, 0.85, 0.05]), k_s=0.4, p=50)
    objects.append(pacman(pac_c, pac_r, yellow))
    objects.append(Sphere(pac_c + vec([0.18, 0.28, 0.3]), 0.06, Material(vec([0.01, 0.01, 0.01]), k_s=0.5, p=80)))

    # row of pellets ahead of him, plus one glowing glass power pellet at the end
    pellet = Material(vec([1.0, 0.85, 0.7]), k_s=0.3, p=40, k_a=vec([1.5, 1.3, 1.0]))
    for i in range(4):
        objects.append(Sphere(vec([0.2 + 0.38 * i, -0.4, 0]), 0.07, pellet))
    objects.append(Sphere(vec([1.75, -0.33, 0]), 0.17, Glass(1.5, tint=(1.0, 0.85, 0.6))))

    # ghosts chasing from behind: colored glass (refraction + Fresnel)
    red_c = (-1.9, -0.05, -0.2)
    cyan_c = (-3.0, -0.05, 0.25)
    objects.append(ghost(red_c, 0.42, Glass(1.5, tint=(1.0, 0.25, 0.25))))
    objects.append(ghost(cyan_c, 0.42, Glass(1.5, tint=(0.3, 0.95, 1.0))))
    objects += eyes(red_c, 0.42, +1)
    objects += eyes(cyan_c, 0.42, +1)

    scene = Scene(objects, bg_color=vec([0.18, 0.07, 0.35]))

    # neon lighting: warm key from the front, blue fill from the side, magenta rim from behind
    lights = [
        PointLight(vec([3, 4, 4]), vec([45, 40, 32])),
        PointLight(vec([-1, 2.5, 3]), vec([4, 8, 25])),
        PointLight(vec([-4, 3, -3]), vec([20, 4, 18])),
        AmbientLight(0.06),
    ]
    camera = Camera(vec([3.6, 0.6, 2.9]), target=vec([-0.8, -0.2, 0]), vfov=32, aspect=16 / 9)
    return camera, scene, lights


if __name__ == "__main__":
    render(*build_scene())
