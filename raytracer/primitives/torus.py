"""Torus primitive. Owner: TODO"""


class Torus:
    def __init__(self, center, axis, major_radius, minor_radius, material):
        # TODO: store parameters / build local frame
        pass

    def intersect(self, ray):
        # TODO: transform ray to local space, solve quartic,
        # return nearest positive hit (t, point, normal) or None
        raise NotImplementedError
