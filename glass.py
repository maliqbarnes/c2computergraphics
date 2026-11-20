"""Refraction and Fresnel. Owner: Person B

Glass is used as a surface's material, e.g. Sphere(c, r, Glass(1.5)).
ray.shade() has one hook so it calls Glass.shade instead of Phong.

Things to know about our ray.py:
- Camera.generate_ray does NOT normalize directions; normalize before
  using reflect/refract/fresnel.
- Sphere and Triangle normals always point outward, even when the ray
  starts inside, so Glass.shade decides entering vs. exiting itself.
- PointLight shadow rays treat glass as opaque (solid shadows). Fine for
  the demos; mention it as a limitation in the presentation.
"""
import numpy as np

from ray import Ray


def reflect(d, n):
    """Mirror a direction about a surface normal.

    Parameters:
      d : (3,) -- unit direction of the incoming ray
      n : (3,) -- unit surface normal
    Return:
      (3,) -- the reflected direction (also unit length)
    """
    # same formula as the mirror ray in ray.shade: flip the part of d that goes along n
    return d - 2 * np.dot(d, n) * n


def refract(d, n, n1, n2):
    """Bend a direction through a surface using Snell's law.

    Parameters:
      d : (3,) -- unit direction of the incoming ray
      n : (3,) -- unit surface normal, facing against d (so dot(d, n) <= 0)
      n1 : float -- index of refraction on the side the ray comes from
      n2 : float -- index of refraction on the side the ray goes into
    Return:
      (3,) -- the refracted direction (unit length), or None on total internal reflection
    """
    # overall idea:
    # 1. get cos of the incoming angle (n faces against d so flip the sign)
    # 2. snell's law (n1 sin_i = n2 sin_t) gives sin^2 of the outgoing angle
    # 3. if sin^2 > 1 then there is no outgoing angle, so its total internal reflection
    # 4. otherwise build the new dir from a part along d and a part along n
    ratio = n1 / n2

    # step 1
    cos_i = -np.dot(d, n)

    # step 2
    sin2_t = ratio*ratio * (1 - cos_i*cos_i)

    # step 3
    if sin2_t > 1:
      return None

    # step 4
    cos_t = np.sqrt(1 - sin2_t)
    return ratio * d + (ratio * cos_i - cos_t) * n


def fresnel_schlick(cos_theta, n1, n2):
    """Fraction of light that reflects (vs. refracts) at a surface.

    Parameters:
      cos_theta : float -- cos of the angle from the normal, measured on the less dense side
      n1, n2 : float -- indices of refraction on the two sides
    Return:
      float -- reflectance in [0, 1]
    """
    # r0 is the reflectance looking straight on (about 4% for glass)
    # it goes up to 1 as the angle gets close to grazing (cos_theta -> 0)
    r0 = ((n1 - n2) / (n1 + n2)) ** 2
    return r0 + (1 - r0) * (1 - cos_theta) ** 5


class Glass:
    def __init__(self, ior=1.5, tint=(1.0, 1.0, 1.0)):
        """Create a glass material.

        Parameters:
          ior : float -- index of refraction, relative to whatever is outside the object
                (1.5 for glass in air; an air bubble inside glass would be 1/1.5)
          tint : (3,) -- RGB color multiplied into light that passes through the surface
        """
        self.ior = ior
        self.tint = np.array(tint, np.float32)

    def shade(self, ray, hit, scene, lights, depth, shade_fn, max_depth):
        """Compute the color seen at a glass surface.

        Parameters:
          ray : Ray -- the ray that hit the surface
          hit : Hit -- the hit data
          scene : Scene -- the scene, for tracing the new rays
          lights : [PointLight or AmbientLight] -- the lights
          depth : int -- the recursion depth so far
          shade_fn : function -- ray.shade, passed in so this file doesn't import it
          max_depth : int -- stop recursing (return black) at this depth
        Return:
          (3,) -- the color seen along this ray
        """
        # overall idea:
        # 0. normalize the ray direction (generate_ray doesnt)
        # 1. figure out if the ray is entering or exiting, flip n and swap n1/n2 if exiting
        # 2. get the reflected and refracted directions
        # 3. trace both rays and shade what they hit (black once we hit the depth limit)
        # 4. blend them with fresnel_schlick (all reflection on TIR) and tint the refracted part

        # same depth rule as mirror rays in ray.shade
        if depth >= max_depth:
          return np.zeros(3)

        # step 0
        d = ray.direction / np.linalg.norm(ray.direction)

        # step 1
        n = hit.normal
        if np.dot(d, n) < 0:
          # entering: coming from outside into the glass
          n1, n2 = 1.0, self.ior
        else:
          # exiting: the outward normal points the same way as d, so flip it to face against d
          n = -n
          n1, n2 = self.ior, 1.0

        # step 2
        refl_dir = reflect(d, n)
        refr_dir = refract(d, n, n1, n2)

        # step 3
        # nudge the start point along each new dir so the ray doesnt hit the same surface again
        refl_ray = Ray(hit.point + 1e-4 * refl_dir, refl_dir)
        refl_color = shade_fn(refl_ray, scene.intersect(refl_ray), scene, lights, depth + 1)

        # total internal reflection: no refracted ray, so all of the light reflects
        if refr_dir is None:
          return refl_color

        refr_ray = Ray(hit.point + 1e-4 * refr_dir, refr_dir)
        refr_color = shade_fn(refr_ray, scene.intersect(refr_ray), scene, lights, depth + 1)

        # step 4
        # schlick needs the angle on the less dense side: when going from glass to air
        # thats the outgoing angle, not the incoming one
        if n1 <= n2:
          cos_theta = -np.dot(d, n)
        else:
          cos_theta = -np.dot(refr_dir, n)
        R = fresnel_schlick(cos_theta, n1, n2)

        # tint only the light that goes through the surface, so reflections stay white
        return R * refl_color + (1 - R) * self.tint * refr_color
