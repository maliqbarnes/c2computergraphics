"""Constructive solid geometry built on A4's Sphere. Owner: Person A

A CSG object goes in Scene(surfs) like any other surface: it only needs
intersect(ray) -> Hit. Internally, children report every interval where
the ray is inside them, as a list of (t_in, hit_in, t_out, hit_out).

Things to know about our ray.py:
- Sphere.intersect already has the quadratic; sphere_intervals needs both
  roots (t0, t1), not just the nearest one.
- Ray directions are not unit length; that's fine for t, but normalize
  normals.
- Shadow rays and reflection rays call Scene.intersect -> CSG.intersect, so
  respect ray.start / ray.end there or you'll get self-shadowing.
"""
import numpy as np

from ray import Hit, Sphere, no_hit


def sphere_intervals(sphere, ray):
    """Return [(t_in, hit_in, t_out, hit_out)] for ray through sphere, or []."""
    e = ray.origin - sphere.center
    d = ray.direction
    a = np.dot(d, d)
    b = 2 * np.dot(d, e)
    c = np.dot(e, e) - sphere.radius ** 2

    disc = b * b - 4 * a * c
    if disc < 0:
        return []

    sq = np.sqrt(disc)
    t0 = (-b - sq) / (2 * a)
    t1 = (-b + sq) / (2 * a)

    def make_hit(t):
        p = ray.origin + t * ray.direction
        n = (p - sphere.center) / sphere.radius
        return Hit(t, p, n, sphere.material)

    return [(t0, make_hit(t0), t1, make_hit(t1))]


class HalfSpace:
    """The half of space behind a plane (dot(x - point, normal) <= 0).

    Two half-spaces intersected = an infinite wedge, useful for the
    Pac-Man mouth.
    """

    def __init__(self, point, normal, material):
        self.point = np.array(point, np.float64)
        self.normal = np.array(normal, np.float64)
        self.normal /= np.linalg.norm(self.normal)
        self.material = material


def halfspace_intervals(plane, ray):
    """Return the interval where the ray is inside the half-space, or []."""
    denom = np.dot(ray.direction, plane.normal)
    to_plane = plane.point - ray.origin

    if abs(denom) < 1e-10:
        # Ray parallel to plane: inside if origin is behind it
        if np.dot(to_plane, plane.normal) >= 0:
            # inside: (-inf, +inf); clamp to ray limits
            inf_hit = Hit(np.inf, None, -plane.normal, plane.material)
            neg_hit = Hit(-np.inf, None, plane.normal, plane.material)
            return [(-np.inf, neg_hit, np.inf, inf_hit)]
        return []

    t = np.dot(to_plane, plane.normal) / denom
    p = ray.origin + t * ray.direction

    # Normal on the plane face always points outward (away from inside)
    if denom > 0:
        # Ray exits the half-space at t; it was inside from -inf to t
        exit_hit = Hit(t, p, plane.normal, plane.material)
        enter_hit = Hit(-np.inf, None, -plane.normal, plane.material)
        return [(-np.inf, enter_hit, t, exit_hit)]
    else:
        # Ray enters the half-space at t; inside from t to +inf
        enter_hit = Hit(t, p, -plane.normal, plane.material)
        exit_hit = Hit(np.inf, None, plane.normal, plane.material)
        return [(t, enter_hit, np.inf, exit_hit)]


def intervals(surf, ray):
    """Dispatch to the right interval function."""
    if isinstance(surf, Sphere):
        return sphere_intervals(surf, ray)
    if isinstance(surf, HalfSpace):
        return halfspace_intervals(surf, ray)
    if isinstance(surf, CSG):
        return surf.intervals(ray)
    raise TypeError(f"CSG does not support {type(surf).__name__}")


def combine(op, a, b):
    """Merge two sorted interval lists for 'union', 'intersection', or 'difference'.

    Each interval is (t_in, hit_in, t_out, hit_out).
    For 'difference', surfaces that belong to shape B have their normals
    flipped because we're seeing the inside of B.
    """
    # Collect all boundary events: (t, is_enter, from_b, hit)
    events = []
    for (t0, h0, t1, h1) in a:
        events.append((t0, True,  False, h0))
        events.append((t1, False, False, h1))
    for (t0, h0, t1, h1) in b:
        events.append((t0, True,  True, h0))
        events.append((t1, False, True, h1))

    events.sort(key=lambda e: e[0])

    in_a = False
    in_b = False
    result = []
    cur_t = None
    cur_hit = None

    def inside(ia, ib):
        if op == "union":
            return ia or ib
        if op == "intersection":
            return ia and ib
        if op == "difference":
            return ia and not ib

    def maybe_flip(hit, from_b):
        """Flip normal on a B-surface for the difference operation."""
        if op == "difference" and from_b and hit.normal is not None:
            return Hit(hit.t, hit.point, -hit.normal, hit.material)
        return hit

    for (t, is_enter, from_b, hit) in events:
        was_inside = inside(in_a, in_b)

        if from_b:
            in_b = is_enter
        else:
            in_a = is_enter

        now_inside = inside(in_a, in_b)

        if not was_inside and now_inside:
            cur_t = t
            cur_hit = maybe_flip(hit, from_b)

        elif was_inside and not now_inside:
            result.append((cur_t, cur_hit, t, maybe_flip(hit, from_b)))
            cur_t = None
            cur_hit = None

    return result



class CSG:
    def __init__(self, op, left, right, material=None):
        assert op in ("union", "intersection", "difference")
        self.op = op
        self.left = left
        self.right = right
        self.material = material  # if set, overrides child materials

    def intervals(self, ray):
        return combine(
            self.op,
            intervals(self.left, ray),
            intervals(self.right, ray),
        )

    def intersect(self, ray):
        """Return the nearest Hit in [ray.start, ray.end], or no_hit."""
        for (t_in, h_in, t_out, h_out) in self.intervals(ray):
            # Pick the first surface point in the valid range
            for t, h in ((t_in, h_in), (t_out, h_out)):
                if ray.start < t <= ray.end and h.point is not None:
                    if self.material is not None:
                        h = Hit(h.t, h.point, h.normal, self.material)
                    return h
        return no_hit
