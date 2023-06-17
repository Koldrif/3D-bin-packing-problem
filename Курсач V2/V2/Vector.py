import enum
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


    def __repr__(self):
        return f"x: {self.x}, y: {self.y}, z: {self.z}"


def reflect_x(vector: Vector3D):
    return Vector3D(vector.x, vector.y * -1, vector.z * -1)


def reflect_y(vector: Vector3D):
    return Vector3D(vector.x * -1, vector.y, vector.z * -1)


def reflect_z(vector: Vector3D):
    return Vector3D(vector.x * -1, vector.y * -1, vector.z)


def reflect_xy(vector: Vector3D):
    return Vector3D(vector.x, vector.y, vector.z * -1)


def reflect_xz(vector: Vector3D):
    return Vector3D(vector.x, vector.y * -1, vector.z)


def reflect_yz(vector: Vector3D):
    return Vector3D(vector.x * -1, vector.y, vector.z)

def no_reflect(vector: Vector3D):
    return Vector3D(vector.x, vector.y, vector.z)


reflection_dictionary = {
    "reflect_x" : reflect_x,
    "reflect_y" : reflect_y,
    "reflect_z" : reflect_z,
    "reflect_xy" : reflect_xy,
    "reflect_xz" : reflect_xz,
    "reflect_yz" : reflect_yz,
    "no_reflect" : no_reflect
}