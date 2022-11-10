

def getZ (Plane):
    return Plane.Origin.Z

Count = 10
Tolerance = 0.01


# # dataDict = {}
# if read:
#     with open(path, "r") as f:
#         dataDict = json.load(f)

initPlanes =  list(data.Branch(count%10))
targetPlanes = list(data.Branch((count+1)%10))
    
# for i in dataDict[str(count%Count)]:
#     initPlanes.append(cv.plane_to_rhino(cg.Plane.from_jsonstring(i)))
# for i in dataDict[str((count+1)%Count)]:
#     targetPlanes.append(cv.plane_to_rhino(cg.Plane.from_jsonstring(i))) 

iterations = 0

keepPlanes = []
removePlanes = []
for n, p in enumerate(initPlanes):
    temp = True
    for m, i in enumerate(targetPlanes):
        iterations +=1
        if p.Origin.DistanceTo(i.Origin) < Tolerance:
            # initPlanes.pop(n)
            targetPlanes.pop(m) 
            temp =False
            keepPlanes.append(p)
            break
    if temp == True: removePlanes.append(p)

removePlanes.sort(key=getZ, reverse= True)
targetPlanes.sort(key=getZ, reverse= False)


print (iterations)

outTemp = keepPlanes


initVisual = initPlanes
targetVisual = targetPlanes