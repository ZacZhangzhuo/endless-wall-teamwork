

import rhinoscriptsyntax as rs
import compas
import compas_rhino
import simple_comm as comm
import Rhino.Geometry as rg

def rhino_to_robot_space(rhino_plane):
    plane = rhino_plane.Clone()
    rhino_matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,robot_base_plane)
    plane.Transform(rhino_matrix)
    return plane

def robot_space_to_rhino (robot_plane):
    plane = robot_plane.Clone()
    robot_matrix = rg.Transform.PlaneToPlane(robot_base_plane,rg.Plane.WorldXY)
    plane.Transform(robot_matrix)
    return plane

reload(comm)

if listen:
    chunks = comm.listen_to_robot("192.168.10.10")
    config = chunks["actual_joints"]
    pose = chunks["pose"]


    
    
pose = compas.geometry.Frame.from_axis_angle_vector([pose[3],pose[4],pose[5]],[pose[0]*1000,pose[1]*1000,pose[2]*1000])
pose = compas_rhino.conversions.frame_to_rhino(pose)

pose = robot_space_to_rhino (pose)