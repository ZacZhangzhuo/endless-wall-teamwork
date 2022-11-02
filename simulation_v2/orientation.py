

import Rhino.Geometry as rg
import math
from copy import deepcopy
scale = rg.Transform.Scale(rg.Plane.WorldXY, 1000,1000,1000)
for v in visual:
    v.Transform(scale)
    
frames[-1].Transform(scale)

for mesh in visual:
    mesh.Transform(rg.Transform.PlaneToPlane(transformation_plane, rg.Plane.WorldXY))

# temp_frame = deepcopy(frames[-1])


frames[-1].Transform(rg.Transform.PlaneToPlane(transformation_plane, rg.Plane.WorldXY))

end_effector.Transform(rg.Transform.PlaneToPlane(transformation_plane, frames[-1] ))

frames[-1].Transform(rg.Transform.Translation(frames[-1].ZAxis * 80))

visual.append(end_effector)
robot_meshs =visual
endeffector_plane = frames[-1]
