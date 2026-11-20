"""Constructive solid geometry. Owner: TODO

Each child must report all ray entry/exit intervals, not just the nearest hit.
"""


class CSG:
    UNION, INTERSECTION, DIFFERENCE = "union", "intersection", "difference"

    def __init__(self, op, left, right):
        self.op, self.left, self.right = op, left, right

    def intervals(self, ray):
        # TODO: combine left/right interval lists according to self.op
        raise NotImplementedError

    def intersect(self, ray):
        # TODO: first positive entry from self.intervals(ray)
        raise NotImplementedError
