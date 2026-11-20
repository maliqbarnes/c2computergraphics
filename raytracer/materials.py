"""Refraction and Fresnel. Owner: Person B"""


def reflect(direction, normal):
    # TODO(B)
    raise NotImplementedError


def refract(direction, normal, n1, n2):
    # TODO(B): Snell's law. Return the refracted direction,
    # or None on total internal reflection.
    raise NotImplementedError


def fresnel_schlick(cos_theta, n1, n2):
    # TODO(B): Schlick approximation of reflectance.
    raise NotImplementedError


class Glass:
    def __init__(self, ior=1.5, tint=(1.0, 1.0, 1.0)):
        self.ior, self.tint = ior, tint

    def shade(self, ray, hit, scene, depth):
        # TODO(B): decide entering vs. exiting, trace reflected and refracted
        # rays (respect the depth limit), blend with the Fresnel term.
        # Hook into wherever A4 computes a material's color.
        raise NotImplementedError
