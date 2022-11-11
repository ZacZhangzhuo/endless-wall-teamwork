from imp import reload
import Rhino.Geometry as rg
import simple_ur_script as ur
# reload(ur)
import simple_comm as c
# reload(c)

def tcp(script):
    script += ur.set_tcp_by_angles(TCP[0], TCP[1], TCP[2], TCP[3], TCP[4], TCP[5])
    return script


def set_robot_base():
    pt_0 = TABLE_NAVIGATION_POINTS[0]  # base plane origin
    pt_1 = TABLE_NAVIGATION_POINTS[1]
    pt_2 = TABLE_NAVIGATION_POINTS[2]
    robot_base = rg.Plane(pt_0, pt_1 - pt_0, pt_2 - pt_0)
    return robot_base


def rhino_to_robot_space(rhino_plane):
    plane = rhino_plane.Clone()
    robot_base_plane = set_robot_base()
    rhino_matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, robot_base_plane)
    plane.Transform(rhino_matrix)
    return plane


def pickup_brick(script, pick_up_plane):
    planes = []
    # change the distance if needed

    safe_plane = pick_up_plane.Clone()
    safe_plane.Translate(rg.Vector3d.ZAxis * SAFE_DIST)

    ## add to the path: go to the safe plane
    script += ur.move_l(safe_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(safe_plane)

    ## add to the path: go to the pick up plane
    script += ur.move_l(pick_up_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(pick_up_plane)

    ## add to the path: turn on the vacuum and wait 1 sec.
    script += ur.set_digital_out(IO, True)
    script += ur.sleep(SAFE_SLEEP_TIME)

    # add to the path: go back to the safe_plane
    script += ur.move_l(safe_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(safe_plane)
    return script, planes

def glue(script, gluePlane):
    planes = []
    safeGluePlane = gluePlane.Clone()
    safeGluePlane.Translate(rg.Vector3d.ZAxis * SAFE_DIST)
    
    script += ur.move_l(safeGluePlane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(safeGluePlane) 
    script += ur.move_l(gluePlane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL) 
    planes.append(gluePlane) 
    script += ur.sleep(SAFE_SLEEP_TIME)
    script += ur.move_l(safeGluePlane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(safeGluePlane) 
    return script, planes


def place_brick(script, place_plane):

    planes = []

    safe_plane = place_plane.Clone()
    safe_plane.Translate(rg.Vector3d.ZAxis * SAFE_DIST)

    # add to the path: go to the safe plane
    script += ur.move_l(safe_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(safe_plane)

    # add to the path: go to the place plane
    script += ur.move_l(place_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(place_plane)

    ## add to the path: turn off the vacuum and wait 1 second (hold the brick)
    script += ur.set_digital_out(IO, False)
    script += ur.sleep(SAFE_SLEEP_TIME)
    # add to the path: go back to the safe plane
    script += ur.move_l(safe_plane, SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    planes.append(safe_plane)

    return script, planes

test_plane = debug_plane.Clone()
# the_stop_plane = stop_plane.Clone()
# stop_configurations.reverse()

def send(script):
    script = c.concatenate_script(script)
    c.send_script(script, ROBOT_IP)
    return script

if count == None: count = 0

script = ""
script = tcp(script)

if is_debug_mode:
    script += ur.move_l(rhino_to_robot_space(test_plane), SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
    

else:
    if count < len(brick_planes):
        script, p = pickup_brick(
            script, rhino_to_robot_space(picking_planes[count % len(picking_planes)])
        )
        script, p = glue( script, rhino_to_robot_space(gluePlane))
        script, p = place_brick(script, rhino_to_robot_space(brick_planes[count]))
        # script += ur.move_l(rhino_to_robot_space(the_stop_plane), SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
        script += ur.move_j(stop_configurations, SAFE_ROBOT_ACC*5, SAFE_ROBOT_VEL*5)
        
    else:
        if len(continuous_picking_planes) == 0 or len(continuous_brick_planes) ==0:
            pass
        else:
            count = count -  len(brick_planes)

            script, p = pickup_brick(
                script, rhino_to_robot_space(continuous_picking_planes[count % len(continuous_picking_planes)])
            )
            script, p = glue( script, rhino_to_robot_space(gluePlane))
            script, p = place_brick(script, rhino_to_robot_space(continuous_brick_planes[count% len(continuous_brick_planes)]))
            # Zac: add to the path: go to the stop plane
            # script += ur.move_l(rhino_to_robot_space(the_stop_plane), SAFE_ROBOT_ACC, SAFE_ROBOT_VEL)
            script += ur.move_j(stop_configurations, SAFE_ROBOT_ACC*3, SAFE_ROBOT_VEL*3)
            

if fabricate:
    send(script)
