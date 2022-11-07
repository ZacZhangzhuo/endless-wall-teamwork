import simple_comm as comm
import Rhino.Geometry as rg
import math
import compas.geometry as geom
# import 
scale = rg.Transform.Scale(rg.Plane.WorldXY, 1000,1000,1000)
for v in visual:
    v.Transform(scale)


frame = frames[-1]
frame.Transform(scale)
for mesh in visual:
    mesh.Transform(rg.Transform.PlaneToPlane(transformation_plane, rg.Plane.WorldXY))
frame.Transform(rg.Transform.PlaneToPlane(transformation_plane, rg.Plane.WorldXY))
end_effector.Transform(rg.Transform.PlaneToPlane(transformation_plane, rg.Plane.WorldXY))


frame = rg.Plane(frame.Origin, frame.YAxis,frame.XAxis )
frame.Translate(frame.XAxis *  TCP[0])
frame.Translate(frame.YAxis *  TCP[1])
frame.Translate(frame.Normal *  -TCP[2])

end_effector.Transform(rg.Transform.PlaneToPlane( rg.Plane.WorldXY, frame ))



visual.append(end_effector)
robot_meshs =visual
endeffector_plane = frame
