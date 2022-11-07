__author__ = "jiang"
__version__ = "2022.11.03"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino
import math
import copy
#make and reparameterize circle to crv
circle = rg.Circle.ToNurbsCurve(rg.Circle(rg.Point3d(0,0,0),r))
circle.Domain = rg.Interval(0,1)

# make the a point on circle as end point
id_pt = rg.Curve.ChangeClosedCurveSeam(circle,t)

#t value on circle
para = rg.Curve.DivideByCount(circle, div, True)

def remap(value,low1,high1, low2, high2):
    """
    value : original value
    low1 : original value's lower bound
    high1 : original value's upper bound
    low2 : remapped value's lower bound
    high2 : remapped value's upper bound
    """
    remapped_value = low2 + (value - low1) * (high2 - low2) / (high1 - low1)
    return remapped_value

#base points for curv
base_pts = []
for p in para:
    base_pts.append(circle.PointAt(p))

# z_value of upper points
z_value=[]
for i in range(len(base_pts)):
    z_value.append(math.sin(((4*math.pi/len(base_pts))*i)+math.pi*0.5)*r/5)

#upper points for crv
up_pts = copy.deepcopy(base_pts)
for i, pt in enumerate(up_pts):
    tranMatrix = rg.Transform.Translation(rg.Vector3d(0,0,z_value[i]+h))
    pt.Transform(tranMatrix)
    
#add end_pt to close the curve
end_pt= copy.copy(up_pts[0])
up_pts.append(end_pt)
up_crv = rg.Curve.CreateInterpolatedCurve(up_pts, 3,rg.CurveKnotStyle(3))










#def rotate(l, n):
#    return l[n:] + l[:n]
#
#
#... 
#>>> l = [1,2,3,4]
#>>> rotate(l,1)
