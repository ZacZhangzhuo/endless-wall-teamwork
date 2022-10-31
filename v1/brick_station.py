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
ROBOT_IP = "192.168.10.10"
SAFE_ROBOT_ACC = 0.6
SAFE_ROBOT_VEL = 1.0
IO = 0 # 0


sleep_time = 0.2

def tcp(script):
    script += ur.set_tcp_by_angles(0.0, 0.0, 80.0, m.radians(0.0), m.radians(180.0),m.radians(0.0))
    
    return script


def set_robot_base():
    pt_0 = rg.Point3d(-249.62,-750.86,-587.98) # base plane origin
    pt_1 = rg.Point3d(-252.73,-1064.50,-587.82) # point on positive x axis
    pt_2 = rg.Point3d(826.13,-752.45,-587.91) # point on positive xy plane
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
#    safe_plane.Translate(rhinoplane.ZAxis*SAFE_DIST)
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


#location of a pick up station
axisangle = Frame.from_axis_angle_vector([3.249,1.999,-3.591],[677.46,-886.44,-492.82])

pickup_planes = []

for plan in  picking_plans:
    x = rg.Transform.PlaneToPlane(picking_plans[0], plan)
    plan.Transform(x)
    pickup_planes.append(rg.Plane(plan))

# print rhinoplane
# pick_station = rg.Plane(rhinoplane)#Rotate Plane



#  picking_planes


script = ""
#skip this step
script = tcp(script)
vis_planes = []



# translate from rhino to robot_space and iterate through all planes
robot_planes = []

for p in brick_planes:
    r_plane = rhino_to_robot_space(p)
    robot_planes.append(r_plane)


for i in range(len(robot_planes)):
    
    script, p = pickup_brick(script,pickup_planes[i])
    vis_planes.extend(p) #only to visualize the planes
    
    script, p = place_brick(script,robot_planes[i])
    vis_planes.extend(p)


if fabricate:
    send(script)

