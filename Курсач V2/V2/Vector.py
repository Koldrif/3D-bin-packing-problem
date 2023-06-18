import enum
import functools

import numpy as np

# class Reflect(enum):
class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @property
    def vector(self):
        return [self.x, self.y, self.z]

    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )


    def __repr__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}"

# @functools.cache
def reflect_x(vector: Vector3D):
    return Vector3D(vector.x, vector.y * -1, vector.z * -1)

# @functools.cache
def reflect_y(vector: Vector3D):
    return Vector3D(vector.x * -1, vector.y, vector.z * -1)

# @functools.cache
def reflect_z(vector: Vector3D):
    return Vector3D(vector.x * -1, vector.y * -1, vector.z)

# @functools.cache
def reflect_xy(vector: Vector3D):
    return Vector3D(vector.x, vector.y, vector.z * -1)

# @functools.cache
def reflect_xz(vector: Vector3D):
    return Vector3D(vector.x, vector.y * -1, vector.z)

# @functools.cache
def reflect_yz(vector: Vector3D):
    return Vector3D(vector.x * -1, vector.y, vector.z)
# @functools.cache
def no_reflect(vector: Vector3D):
    return Vector3D(vector.x, vector.y, vector.z)


reflection_dictionary = {
    "no_reflect": no_reflect,
    "reflect_x" : reflect_x,
    "reflect_y" : reflect_y,
    "reflect_z" : reflect_z,
    "reflect_xy" : reflect_xy,
    "reflect_xz" : reflect_xz,
    "reflect_yz" : reflect_yz,

}