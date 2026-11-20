# C2 Ray Tracer

Team: TODO
Base: fork of the A4 repo (copy or merge the A4 ray tracer code into `raytracer/`).

## Layout

```
raytracer/
  primitives/     new shapes (torus, cone, ...) – one file per shape
  csg.py          union / intersection / difference
  materials.py    shading models (Fresnel, refraction, ...)
  textures.py     diffuse / normal / bump / displacement mapping
  accel.py        BVH or k-d tree
scenes/
  final.py        main composition
  tests/          one small scene per feature
tools/
  render_tests.py render every test scene into gallery/
  benchmark.py    time a scene with/without acceleration
  combine.py      recombine per-light or interleaved renders
gallery/          output images + markdown notes for the static gallery
DEVLOG.md         dated notes and intermediate results
PROVENANCE.md     sources for code, assets and packages
```

## Run

```
python -m venv .venv && source .venv/bin/activate
python tools/render_tests.py
python scenes/final.py
```
