"""Constructive solid geometry. Owner: Person A

Children must report every interval where the ray is inside them,
not just the nearest hit.
"""


def sphere_intervals(sphere, ray):
    # TODO(A): solve the ray-sphere quadratic and return [(t_in, t_out)],
    # or [] on a miss. Use the A4 sphere's center/radius.
    raise NotImplementedError


def halfspace_intervals(point, normal, ray):
    # TODO(A): interval where the ray is behind the plane (point, normal).
    # Needed for the Pac-Man mouth wedge (intersection of two half-spaces).
    raise NotImplementedError


def combine(op, a, b):
    # TODO(A): merge two sorted interval lists for "union",
    # "intersection" or "difference".
    raise NotImplementedError


class CSG:
    def __init__(self, op, left, right, material):
        self.op, self.left, self.right = op, left, right
        self.material = material

    def intervals(self, ray):
        # TODO(A): combine(self.op, left intervals, right intervals)
        raise NotImplementedError

    def intersect(self, ray):
        # TODO(A): first positive t from self.intervals(ray).
        # Return a hit in A4's format. Flip the normal when the surface
        # comes from the subtracted (right) shape in a difference.
        raise NotImplementedError
