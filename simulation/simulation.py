from imp import reload
import Rhino.Geometry as rg
import simple_ur_script as ur
reload(ur)
import simple_comm as c
reload(c)
import math as m
from compas.geometry import Frame
from compas_rhino.conversions import frame_to_rhino


# change these values if needed
# ROBOT_IP = "192.168.10.10"
SAFE_ROBOT_ACC = 0.1
SAFE_ROBOT_VEL = 0.1
IO = 0 # 0
sleep_time = 0.2

def tcp(script):
    script += ur.set_tcp_by_angles(-0.35, 0.5, 89.08, m.radians(0.0), m.radians(0.0),m.radians(0.0))
    
    return script

def set_robot_base():
    pt_0 = rg.Point3d(-200 ,-320 ,-587.3) # base plane origin
    pt_1 = rg.Point3d(-206.2 ,-192.6 ,-587.3) # point on positive x axis
    pt_2 = rg.Point3d(456.4 ,-326.4 ,-587.3) # point on positive xy plane
    robot_base = rg.Plane(pt_0,pt_1-pt_0,pt_2-pt_0)
    return robot_base

def rhino_to_robot_space(rhino_plane):
    plane = rhino_plane.Clone()
    robot_base_plane = set_robot_base()
    rhino_matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,robot_base_plane)
    plane.Transform(rhino_matrix)
    return plane

def pickup_brick(script,pick_up_plane):
    planes = []
    #change the distance if needed
    SAFE_DIST = 150
    
    safe_plane = pick_up_plane.Clone()
    #safe_plane.Translate(rhinoplane.ZAxis*SAFE_DIST)
    safe_plane.Translate(rg.Vector3d.ZAxis*SAFE_DIST)
    
    ## add to the path: go to the safe plane
    script += ur.move_l(safe_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(safe_plane)
    
    ## add to the path: go to the pick up plane
    script += ur.move_l(pick_up_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(pick_up_plane)
    
    ## add to the path: turn on the vacuum and wait 1 sec.
    script += ur.set_digital_out(IO,True)
    script += ur.sleep(sleep_time)

    # add to the path: go back to the safe_plane
    script += ur.move_l(safe_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(safe_plane)
    return script, planes

def place_brick(script, place_plane):
    
    planes = []
    
    SAFE_DIST = 100
    safe_plane = place_plane.Clone()
    safe_plane.Translate(rg.Vector3d.ZAxis*SAFE_DIST)
    
    # add to the path: go to the safe plane
    script += ur.move_l(safe_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(safe_plane)
    
    # add to the path: go to the place plane
    script += ur.move_l(place_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(place_plane)
    
    ## add to the path: turn off the vacuum and wait 1 second (hold the brick)
    script += ur.set_digital_out(IO,False)
    script += ur.sleep(sleep_time)
    # add to the path: go back to the safe plane
    script += ur.move_l(safe_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(safe_plane)
    
    return script,planes

def send(script):
    script = c.concatenate_script(script)
    c.send_script(script, ROBOT_IP)
    return script 

script = ""
script = tcp(script)

#! ---------------------------------------------------------------- Test and navigation only: go to a point 
test_plane = debug_plane.Clone()
script += ur.move_l(rhino_to_robot_space(test_plane), SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
#! ----------------------------------------------------------------

"""
#!  ---------------------------------------------------------------- Real run
#Optional: location of a pick up station
# pick_point = Frame.from_axis_angle_vector([2.403,2.421,-4.166],[677.46,-886.44,-492.82])

for i in range(len(brick_planes)):
    script, p = pickup_brick(script,picking_planes[i%len(picking_planes)])
    script, p = place_brick(script,robot_planes[i])
#!  ---------------------------------------------------------------- 
"""
#! Never touch
if fabricate:
    send(script)
