"""Acceleration structure (BVH / k-d tree). Owner: TODO"""


class BVH:
    def __init__(self, objects):
        # TODO: build tree over object bounding boxes
        pass

    def intersect(self, ray):
        # TODO: traverse tree, return nearest hit
        raise NotImplementedError
