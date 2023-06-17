import Vector
import functools

class Cuboid:
    # a rectangular solid
    def __init__(self, x0, y0, z0, x1, y1, z1):

        self.z0 = min(z0, z1)
        self.x0 = min(x0, x1)
        self.y0 = min(y0, y1)
        self.z1 = max(z0, z1)
        self.x1 = max(x0, x1)
        self.y1 = max(y0, y1)

        self.start = (self.x0, self.y0, self.z0)
        self.end = (self.x1, self.y1, self.z1)

    def centre(self):
        center_x = (self.x0 + self.x1) / 2
        center_y = (self.y0 + self.y1) / 2
        center_z = (self.z0 + self.z1) / 2
        return (center_x, center_y, center_z)

    def intersects(self, other):
        # returns true if this cuboid intersects with another one
        if self == other:
            return True
        else:
            return (
                    self.x0 <= other.x1
                    and self.x1 >= other.x0
                    and self.y0 <= other.y1
                    and self.y1 >= other.y0
                    and self.z0 <= other.z1
                    and self.z1 >= other.z0
            )


class Item:
    def __init__(self,
                 length: float,
                 width: float,
                 height: float,
                 pivot_point: Vector = Vector.Vector3D(0, 0, 0)):
        self.length = length
        self.width = width
        self.height = height

        self.pivot_point = pivot_point

    @property
    def vector(self):
        return [self.length, self.width, self.height]


    @functools.cached_property
    def volume(self):
        return self.height * self.width * self.length

    @functools.cache
    def to_cuboid(self, pivot_point, rotation) -> Cuboid:
        return Cuboid(
            *pivot_point.vector,
            *rotation(Vector.Vector3D(*self.vector)).vector)

