"""Render every scene in scenes/tests into gallery/<name>/ with a timestamp."""
import datetime
import importlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TESTS = ROOT / "scenes" / "tests"
OUT = ROOT / "gallery"


def main():
    for path in sorted(TESTS.glob("*.py")):
        module = importlib.import_module(f"scenes.tests.{path.stem}")
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        out_dir = OUT / module.NAME
        out_dir.mkdir(parents=True, exist_ok=True)
        # TODO: scene = module.build_scene(); render and save to out_dir / f"{stamp}.png"
        (out_dir / "notes.md").write_text(f"# {module.NAME}\n\n{module.DESCRIPTION}\n")
        print(f"{module.NAME} -> {out_dir}")


if __name__ == "__main__":
    main()
