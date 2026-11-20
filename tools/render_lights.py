"""Lighting exploration for the final scene.

Renders each light of scenes/final.py on its own once (saved as .npy), then
recombines them with weights without re-tracing:

    python tools/render_lights.py render --nx 480
    python tools/render_lights.py combine 1.0 0.6 0.3
"""
import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.argv, argv = sys.argv[:1], sys.argv[1:]  # keep cli.py's parser from reading our args

import numpy as np
from PIL import Image

from ray import render_image
from utils import to_srgb8
from combine import weighted_sum
from scenes.final import build_scene

OUT = ROOT / "gallery" / "lighting"


def render(nx):
    camera, scene, lights = build_scene()
    ny = int(round(nx / camera.aspect))
    OUT.mkdir(parents=True, exist_ok=True)
    for i, light in enumerate(lights):
        img = render_image(camera, scene, [light], nx, ny)
        np.save(OUT / f"light{i}.npy", img)
        print(f"light{i}: {type(light).__name__}")


def combine(weights):
    images = [np.load(p) for p in sorted(OUT.glob("light*.npy"))]
    out = weighted_sum(images, weights)
    name = "combined_" + "_".join(f"{w:g}" for w in weights) + ".png"
    Image.fromarray(to_srgb8(out), "RGB").save(OUT / name)
    print(OUT / name)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render"); r.add_argument("--nx", type=int, default=480)
    c = sub.add_parser("combine"); c.add_argument("weights", type=float, nargs="+")
    a = p.parse_args(argv)
    render(a.nx) if a.cmd == "render" else combine(a.weights)
