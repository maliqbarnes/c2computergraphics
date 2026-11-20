"""Time a scene with and without the acceleration structure."""
import time


def time_render(render_fn):
    start = time.perf_counter()
    render_fn()
    return time.perf_counter() - start


if __name__ == "__main__":
    # TODO: plug in render with/without BVH and print both times
    pass
