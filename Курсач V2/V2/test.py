# import Vector
# from Vector import *
# vec = Vector3D(1, 2, 3)

# print(vec)

# for key, val in Vector.reflection_dictionary.items():
# #     print(key, val(vec))


# import fcl
# import numpy as np


# g1 = fcl.Box(1,1,1)
# t1 = fcl.Transform()
# o1 = fcl.CollisionObject(g1, t1)

# g2 = fcl.Box(.5,.5,.5)
# t2 = fcl.Transform()
# o2 = fcl.CollisionObject(g2, t2)

# request = fcl.CollisionRequest()
# result = fcl.CollisionResult()

# ret = bool(fcl.collide(o1, o2, request, result))
# print(ret)

a = {1: 1, 2 : 2}
a[0] = 0

print(a[0])