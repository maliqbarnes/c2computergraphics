"""Texture, normal and bump mapping. Owner: TODO"""


class ImageTexture:
    def __init__(self, path):
        # TODO: load image
        pass

    def sample(self, u, v):
        # TODO: bilinear lookup
        raise NotImplementedError


def perturb_normal(normal, tangent, bitangent, map_value):
    # TODO
    raise NotImplementedError
