import numpy as np

from utils import *

"""
Core implementation of the ray tracer.  This module contains the classes (Sphere, Mesh, etc.)
that define the contents of scenes, as well as classes (Ray, Hit) and functions (shade) used in 
the rendering algorithm, and the main entry point `render_image`.

In the documentation of these classes, we indicate the expected types of arguments with a
colon, and use the convention that just writing a tuple means that the expected type is a
NumPy array of that shape.  Implementations can assume these types are preconditions that
are met, and if they fail for other type inputs it's an error of the caller.  (This might 
not be the best way to handle such validation in industrial-strength code but we are adopting
this rule to keep things simple and efficient.)
"""


class Ray:

    def __init__(self, origin, direction, start=0., end=np.inf):
        """Create a ray with the given origin and direction.

        Parameters:
          origin : (3,) -- the start point of the ray, a 3D point
          direction : (3,) -- the direction of the ray, a 3D vector (not necessarily normalized)
          start, end : float -- the minimum and maximum t values for intersections
        """
        # Convert these vectors to double to help ensure intersection
        # computations will be done in double precision
        self.origin = np.array(origin, np.float64)
        self.direction = np.array(direction, np.float64)
        self.start = start
        self.end = end


class Material:

    def __init__(self, k_d, k_s=0., p=20., k_m=0., k_a=None):
        """Create a new material with the given parameters.

        Parameters:
          k_d : (3,) -- the diffuse coefficient
          k_s : (3,) or float -- the specular coefficient
          p : float -- the specular exponent
          k_m : (3,) or float -- the mirror reflection coefficient
          k_a : (3,) -- the ambient coefficient (defaults to match diffuse color)
        """
        self.k_d = k_d
        self.k_s = k_s
        self.p = p
        self.k_m = k_m
        self.k_a = k_a if k_a is not None else k_d


class Hit:

    def __init__(self, t, point=None, normal=None, material=None):
        """Create a Hit with the given data.

        Parameters:
          t : float -- the t value of the intersection along the ray
          point : (3,) -- the 3D point where the intersection happens
          normal : (3,) -- the 3D outward-facing unit normal to the surface at the hit point
          material : (Material) -- the material of the surface
        """
        self.t = t
        self.point = point
        self.normal = normal
        self.material = material

# Value to represent absence of an intersection
no_hit = Hit(np.inf)


class Sphere:

    def __init__(self, center, radius, material):
        """Create a sphere with the given center and radius.

        Parameters:
          center : (3,) -- a 3D point specifying the sphere's center
          radius : float -- a Python float specifying the sphere's radius
          material : Material -- the material of the surface
        """
        self.center = center
        self.radius = radius
        self.material = material

    def intersect(self, ray):
        """Computes the first (smallest t) intersection between a ray and this sphere.

        Parameters:
          ray : Ray -- the ray to intersect with the sphere
        Return:
          Hit -- the hit data
        """
        # TODO A4 implement this function
        # need to start with setting up the quadratic equarion
        # then will check the discriminant for intersection
        # then get both roots and return the one that is nearest to origin of ray
        e = ray.origin - self.center
        d = ray.direction
        a = np.dot(d,d)
        b = 2 * np.dot(d, e)
        c = np.dot(e, e) - self.radius*self.radius

        discriminant = b*b - 4*a*c
        if discriminant < 0:
          return no_hit
        else:
          t0 = (-b - np.sqrt(discriminant)) / (2*a)
          t1 = (-b + np.sqrt(discriminant)) / (2*a)
          # a is > 0 so then t0 <= t1, no need to sort them
        
        if t0 > ray.end or t1 < ray.start:
          return no_hit

        t = t0 if t0 >= ray.start else t1
        if t > ray.end:
          return no_hit
        point = ray.origin + t * ray.direction
        normal = (point - self.center) / self.radius
        
        return Hit(t, point, normal, self.material)


class Triangle:

    def __init__(self, vs, material):
        """Create a triangle from the given vertices.

        Parameters:
          vs (3,3) -- an arry of 3 3D points that are the vertices (CCW order)
          material : Material -- the material of the surface
        """
        self.vs = vs
        self.material = material

    def intersect(self, ray):
        """Computes the intersection between a ray and this triangle, if it exists.

        Parameters:
          ray : Ray -- the ray to intersect with the triangle
        Return:
          Hit -- the hit data
        """
        # TODO A4 implement this function
        # overall idea: any point in triangle can be a lin combo of the vertices
        # we can set up a systems of equations to solve for coeffs
        v0 = self.vs[0]
        v1 = self.vs[1]
        v2 = self.vs[2]

        origin = ray.origin
        direction = ray.direction

        e1 = v1 - v0
        e2 = v2 - v0
        vec1 = origin - v0
        determinant = np.linalg.det(np.array([e1, e2, -direction]).T)
        if determinant == 0:
          return no_hit
        
        vec2 = np.array([np.linalg.det(np.array([vec1, e2, -direction]).T)])
        beta = vec2 / determinant
        if beta < 0 or beta > 1:
          return no_hit

        vec3 = np.array([np.linalg.det(np.array([e1, vec1, -direction]).T)])
        gamma = vec3 / determinant
        if gamma < 0 or beta + gamma > 1:
          return no_hit
        
        t = np.linalg.det(np.array([e1, e2, vec1]).T) / determinant
        if t < ray.start or t > ray.end:
          return no_hit
        
        point = origin + t*direction
        norm = np.cross(e1,e2)
        return Hit(t, point, norm/np.linalg.norm(norm), self.material)




class Camera:

    def __init__(self, eye=vec([0,0,0]), target=vec([0,0,-1]), up=vec([0,1,0]), 
                 vfov=90.0, aspect=1.0):
        """Create a camera with given viewing parameters.

        Parameters:
          eye : (3,) -- the camera's location, aka viewpoint (a 3D point)
          target : (3,) -- where the camera is looking: a 3D point that appears centered in the view
          up : (3,) -- the camera's orientation: a 3D vector that appears straight up in the view
          vfov : float -- the full vertical field of view in degrees
          aspect : float -- the aspect ratio of the camera's view (ratio of width to height)
        """
        # TODO A4 implement this constructor to store whatever you need for ray generation
        self.eye = eye
        self.aspect = aspect

        # start with camera basis
        w = (eye - target) / np.linalg.norm(eye - target) # the unit vec from target to eye
        u = np.cross(up, w) / np.linalg.norm(np.cross(up, w)) # the unit vec from cross of up and w
        v = np.cross(w,u) # just the cross of w, u

        # now need focal dist, need the plan to be from -1,1 in y
        self.f = 1 / np.tan(np.radians(vfov) / 2)

        # camera basis matrix
        self.M = np.eye(4);  # set this to the matrix that transforms your camera's coordinate system to world coordinates
        self.M[:3, 0] = u
        self.M[:3, 1] = v
        self.M[:3, 2] = w
        self.M[:3, 3] = eye


    def generate_ray(self, img_point):
        """Compute the ray corresponding to a point in the image.

        Parameters:
          img_point : (2,) -- a 2D point in [0,1] x [0,1], where (0,0) is the upper left
                      corner of the image and (1,1) is the lower right.
        Return:
          Ray -- The ray corresponding to that image location (not necessarily normalized)
        """
        # TODO A4 implement this function
        # overall idea here:
        # 1. split the input (aka get the x,y values from img_point)
        # 2. get the horizontal position of the plane
        # 3. get the vertical position of the plane
        # 4. build the camera space direction
        # 5. rotate it to world
        # 6. return ray
        x = img_point[0]
        y = img_point[1]

        xc = (2*x - 1) * self.aspect
        yc = 1 - 2*y
        zc = -self.f

        # the vector [xc,yc,-f] is in camera space, need to transform to world w rotation of M
        dcam = np.array([xc, yc, zc])
        dworld = self.M[:3,:3].dot(dcam)

        return Ray(self.eye, dworld)


class PointLight:

    def __init__(self, position, intensity):
        """Create a point light at given position and with given intensity

        Parameters:
          position : (3,) -- 3D point giving the light source location in scene
          intensity : (3,) or float -- RGB or scalar intensity of the source
        """
        self.position = position
        self.intensity = intensity

    def illuminate(self, ray, hit, scene):
        """Compute the shading at a surface point due to this light.

        Parameters:
          ray : Ray -- the ray that hit the surface
          hit : Hit -- the hit data
          scene : Scene -- the scene, for shadow rays
        Return:
          (3,) -- the light reflected from the surface
        """
        # TODO A4 implement this function
        # overall idea: 
        # 1. find the light direction (get vec from hit point to light and its length, and then the unit length
        # 2. shoot a ray from hit point to light and check if it hits anything before getting to light
        # 3. find the view direction (unit vec from hit point to ray origin)
        # 4. find the half vector (halfway between light and view
        # 5. combine to get final color)
        material = hit.material
        norm = hit.normal

        # step 1
        to_light = self.position - hit.point
        dist = np.linalg.norm(to_light) # the length
        left_dir = to_light / dist # the unit vector

        # part 2
        shadow_ray = Ray(hit.point + 1e-6 * left_dir, left_dir)
        if scene.intersect(shadow_ray).t < dist:
          return vec([0,0,0])

        # part 3
        view = ray.origin - hit.point
        view = view / np.linalg.norm(view) # unit vector

        # part 4
        half_vec = (left_dir + view) / np.linalg.norm(left_dir + view)

        # part 5
        norml = np.dot(norm, left_dir)
        normh = np.dot(norm, half_vec)

        return (material.k_d + material.k_s * max(normh, 0) ** material.p) * max(norml, 0) * self.intensity / dist**2

class AmbientLight:

    def __init__(self, intensity):
        """Create an ambient light of given intensity

        Parameters:
          intensity (3,) or float: the intensity of the ambient light
        """
        self.intensity = intensity

    def illuminate(self, ray, hit, scene):
        """Compute the shading at a surface point due to this light.

        Parameters:
          ray : Ray -- the ray that hit the surface
          hit : Hit -- the hit data
          scene : Scene -- the scene, for shadow rays
        Return:
          (3,) -- the light reflected from the surface
        """
        # TODO A4 implement this function
        # all needed is to return the materials ambient coeff x light intensity
        return hit.material.k_a * self.intensity


class Scene:

    def __init__(self, surfs, bg_color=vec([0.2,0.3,0.5])):
        """Create a scene containing the given objects.

        Parameters:
          surfs : [Sphere, Triangle] -- list of the surfaces in the scene
          bg_color : (3,) -- RGB color that is seen where no objects appear
        """
        self.surfs = surfs
        self.bg_color = bg_color

    def intersect(self, ray):
        """Computes the first (smallest t) intersection between a ray and the scene.

        Parameters:
          ray : Ray -- the ray to intersect with the scene
        Return:
          Hit -- the hit data
        """
        # TODO A4 implement this function
        # overall idea: loop through the surfaces and just find the closest intersection
        closest = no_hit
        for s in self.surfs:
          hit = s.intersect(ray)
          if hit.t < closest.t:
            closest = hit
        return closest


MAX_DEPTH = 4

# anti-aliasing: each pixel shoots an AA_SAMPLES x AA_SAMPLES grid of rays and averages them
# (1 = old behavior, one ray through the center; cost goes up by AA_SAMPLES^2)
AA_SAMPLES = 2

def shade(ray, hit, scene, lights, depth=0):
    """Compute shading for a ray-surface intersection.

    Parameters:
      ray : Ray -- the ray that hit the surface
      hit : Hit -- the hit data
      scene : Scene -- the scene
      lights : [PointLight or AmbientLight] -- the lights
      depth : int -- the recursion depth so far
    Return:
      (3,) -- the color seen along this ray
    When mirror reflection is being computed, recursion will only proceed to a depth
    of MAX_DEPTH, with zero contribution beyond that depth.
    """
    # TODO A4 implement this function
    # main idea:
    # if ray hits nothing, then return the background color
    # if not, then add up the contributson from all lights
    # if the depth limit not at max, then shoot reflection ray and add that 
    # return tot color
    if hit.t == np.inf:
        return scene.bg_color

    # C2: glass doesnt use phong at all (no k_d/k_s/k_a), so hand the whole thing off
    # to Glass.shade, and do it before the lights loop
    # (imported here and not at the top bc glass.py imports Ray from this file)
    from glass import Glass
    if isinstance(hit.material, Glass):
      return hit.material.shade(ray, hit, scene, lights, depth, shade, MAX_DEPTH)
    
    color = np.zeros(3)
    for l in lights:
      color += l.illuminate(ray, hit, scene)
    
    if depth < MAX_DEPTH and np.any(hit.material.k_m >0):
      # then shoot reflection ray
      n = hit.normal
      d = ray.direction - 2 * np.dot(ray.direction, n) * n
      ref_ray = Ray(hit.point + 1e-6 * d, d)
      ref_hit = scene.intersect(ref_ray)
      color += hit.material.k_m * shade(ref_ray, ref_hit, scene, lights, depth + 1)

    return color


def render_image(camera, scene, lights, nx, ny):
    """Render a ray traced image.

    Parameters:
      camera : Camera -- the camera defining the view
      scene : Scene -- the scene to be rendered
      lights : Lights -- the lights illuminating the scene
      nx, ny : int -- the dimensions of the rendered image
    Returns:
      (ny, nx, 3) float32 -- the RGB image
    """
    # TODO A4 implement this function
    # main idea here:
    # create an empty image array
    # loop over each pixel
    # for each pixel:
    # find the center, ask camera for ray through that point, find whaat the ray hits, shade hit to get color, store color
    # C2 anti-aliasing: instead of one ray through the pixel center, split the pixel into an
    # AA_SAMPLES x AA_SAMPLES grid, shoot a ray through the center of each little cell,
    # and average the colors so edges blend instead of looking like stairs
    n = AA_SAMPLES
    output = np.zeros((ny, nx, 3), np.float32)
    for i in range(ny):
      for j in range(nx):
        color = np.zeros(3)
        for si in range(n):
          for sj in range(n):
            point_img = np.array([(j + (sj + 0.5) / n) / nx, (i + (si + 0.5) / n) / ny])
            ray = camera.generate_ray(point_img)
            hit = scene.intersect(ray)
            color += shade(ray,hit,scene,lights)
        output[i,j] = color / (n*n)
    return output