import copy
import Rhino.Geometry as rg
import math

distance = []
for p in x:
    # distance.append(p.DistanceTo(y.Origin)
    distance.append(round(p.ClosestPoint(y.Origin).DistanceTo(y.Origin)))


layers = copy.deepcopy(distance)

xx = list(set(layers))
xx.sort()

temp = -1
for tx in xx:

    for n, d in enumerate(distance):
        if d == tx:
            x[n].Transform(
                rg.Transform.Rotation(temp * math.pi/36, x[n].ZAxis, x[n].Origin)
            )  # angleRadians: float, rotationAxis: Vector3d, rotationCenter: Point3d
    temp = -temp


a = x
# a = layers
