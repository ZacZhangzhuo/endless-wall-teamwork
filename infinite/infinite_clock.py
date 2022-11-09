import json
import compas_rhino.conversions as cv
import compas.geometry as cg
from copy import deepcopy
Count = 10
Tolerance = 0.01


# dataDict = {}
if read:
    with open(path, "r") as f:
        dataDict = json.load(f)

initPlanes = []
targetPlanes = []
for i in dataDict[str(count%Count)]:
    initPlanes.append(cv.plane_to_rhino(cg.Plane.from_jsonstring(i)))
for i in dataDict[str((count+1)%Count)]:
    targetPlanes.append(cv.plane_to_rhino(cg.Plane.from_jsonstring(i))) 

keepPlanes = []
for n, p in enumerate(initPlanes):
    for m, i in enumerate(targetPlanes):
        if p.DistanceTo(i.Origin) < Tolerance:
            targetPlanes.pop(m)
            keepPlanes.append(p)
            break




outTemp = keepPlanes


initVisual = initPlanes
targetVisual = targetPlanes
