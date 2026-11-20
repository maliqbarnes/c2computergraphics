"""Render every scene in scenes/tests into gallery/<name>/."""
import datetime
import importlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TESTS = ROOT / "scenes" / "tests"
OUT = ROOT / "gallery"


def render(scene, path):
    # TODO: call the A4 renderer and save the image to path
    raise NotImplementedError


def main():
    for path in sorted(TESTS.glob("*.py")):
        if path.stem == "__init__":
            continue
        module = importlib.import_module(f"scenes.tests.{path.stem}")
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        out_dir = OUT / module.NAME
        out_dir.mkdir(parents=True, exist_ok=True)
        render(module.build_scene(), out_dir / f"{stamp}.png")
        (out_dir / "notes.md").write_text(f"# {module.NAME}\n\n{module.DESCRIPTION}\n")


if __name__ == "__main__":
    main()
