import math


def getZ(Plane):
    return Plane.Origin.Z


Count = 10
Tolerance = 0.01

RemovePlanes = []
TargetPlanes = []
for count in range(Count):

    # for i in range(
    listLength = 100000000
    for i in range(10):
        length = len(list(data.Branch(i)))
        if length < listLength:
            listLength = length

    initPlanes = list(data.Branch((count) % Count))[:listLength]
    theTargetPlanes = list(data.Branch((count + 1) % Count))[:listLength]

    iterations = 0

    keepPlanes = []
    theRemovePlanes = []
    for n, p in enumerate(initPlanes):
        temp = True
        for m, i in enumerate(theTargetPlanes):
            iterations += 1
            if p.Origin.DistanceTo(i.Origin) < Tolerance:
                # initPlanes.pop(n)
                theTargetPlanes.pop(m)
                temp = False
                keepPlanes.append(p)
                break
        if temp == True:
            theRemovePlanes.append(p)

    theRemovePlanes.sort(key=getZ, reverse=True)
    theTargetPlanes.sort(key=getZ, reverse=False)
    
    RemovePlanes.extend(theRemovePlanes)
    TargetPlanes.extend(theTargetPlanes)
