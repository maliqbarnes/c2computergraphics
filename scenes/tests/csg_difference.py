"""CSG demo: difference.

Subtracts the right sphere from the left, carving out a bite.
Demonstrates Pac-Man mouth: a sphere minus a wedge of half-spaces.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ray import *
from utils import vec
from csg import CSG, HalfSpace

NAME = "csg_difference"
DESCRIPTION = (
    "Difference: left sphere minus right sphere (bite carved out). "
    "Also shows a Pac-Man mouth made from a sphere minus two half-spaces."
)


def build_scene():
    gray    = Material(vec([0.2, 0.2, 0.2]), k_m=0.3)
    yellow  = Material(vec([0.9, 0.8, 0.1]), k_s=0.3, p=40)
    white   = Material(vec([0.9, 0.9, 0.9]))

    # Left: simple sphere-minus-sphere
    base   = Sphere(vec([-1.1, 0, 0]), 0.55, yellow)
    cutter = Sphere(vec([-0.7, 0, 0]), 0.4,  white)
    bitten = CSG("difference", base, cutter)

    # Right: Pac-Man mouth (sphere minus wedge of two half-spaces)
    pacman_body = Sphere(vec([0.9, 0, 0]), 0.55, yellow)
    # Upper lip of mouth: half-space whose normal points downward
    upper = HalfSpace(vec([0.9, 0, 0]), vec([ 0.5, -1, 0]), white)
    # Lower lip: normal points upward
    lower = HalfSpace(vec([0.9, 0, 0]), vec([ 0.5,  1, 0]), white)
    mouth = CSG("intersection", upper, lower)
    pacman = CSG("difference", pacman_body, mouth)

    scene = Scene([
        bitten,
        pacman,
        Sphere(vec([0, -40, 0]), 39.5, gray),
    ])
    lights = [
        PointLight(vec([12, 10, 5]), vec([300, 300, 300])),
        AmbientLight(0.1),
    ]
    camera = Camera(vec([3, 1.7, 5]), target=vec([-0.1, 0, 0]), vfov=28, aspect=16/9)
    return camera, scene, lights
