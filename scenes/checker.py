"""Checkerboard floor used as a backdrop in the refraction demos.

Not a feature, just a helper: a flat, square y = height plane whose material
alternates between two colors, so bending from the glass is easy to see.
"""
import numpy as np

from ray import Hit, no_hit


class CheckerPlane:

    def __init__(self, height, size, mat_a, mat_b, extent=6.0):
        """Create a checkerboard floor.

        Parameters:
          height : float -- y value of the floor
          size : float -- side length of one square
          mat_a, mat_b : Material -- the two alternating materials
          extent : float -- the floor covers -extent <= x, z <= extent
        """
        self.height = height
        self.size = size
        self.mat_a = mat_a
        self.mat_b = mat_b
        self.extent = extent

    def intersect(self, ray):
        """Computes the intersection between a ray and the floor, if it exists.

        Parameters:
          ray : Ray -- the ray to intersect with the floor
        Return:
          Hit -- the hit data
        """
        # overall idea:
        # 1. solve origin.y + t * dir.y = height for t
        # 2. throw it out if its outside the ray's range or off the edge of the floor
        # 3. pick the material from which square the point lands in
        dy = ray.direction[1]
        if dy == 0:
          return no_hit

        # step 1
        t = (self.height - ray.origin[1]) / dy

        # step 2
        if t < ray.start or t > ray.end:
          return no_hit
        point = ray.origin + t * ray.direction
        if abs(point[0]) > self.extent or abs(point[2]) > self.extent:
          return no_hit

        # step 3
        ix = int(np.floor(point[0] / self.size))
        iz = int(np.floor(point[2] / self.size))
        material = self.mat_a if (ix + iz) % 2 == 0 else self.mat_b

        return Hit(t, point, np.array([0.0, 1.0, 0.0]), material)
