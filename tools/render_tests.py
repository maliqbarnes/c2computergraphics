"""Render every scene in scenes/tests into gallery/<name>/<timestamp>.png.

    python tools/render_tests.py            # all
    python tools/render_tests.py csg_union  # one
"""
import datetime
import importlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]

from PIL import Image

from ray import render_image
from utils import to_srgb8

NX, NY = 320, 180


def render(camera, scene, lights, path):
    img = render_image(camera, scene, lights, NX, NY)
    Image.fromarray(to_srgb8(img), "RGB").save(path)


def main(names):
    for path in sorted((ROOT / "scenes" / "tests").glob("*.py")):
        if path.stem == "__init__" or (names and path.stem not in names):
            continue
        module = importlib.import_module(f"scenes.tests.{path.stem}")
        out_dir = ROOT / "gallery" / module.NAME
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        render(*module.build_scene(), out_dir / f"{stamp}.png")
        (out_dir / "notes.md").write_text(f"# {module.NAME}\n\n{module.DESCRIPTION}\n")
        print(module.NAME)


if __name__ == "__main__":
    main(ARGS)
