import math
import scriptcontext as rs

fabricate = run

if x: rs.sticky["count"] -=1
if reset:
    rs.sticky["count"] = 0

temp = 0
for i in range(len(current_configuration)):
    if round(current_configuration[i], 1) == round(stop_configuration[i], 1):
        temp += 1

if temp == 6:
    rs.sticky["count"] += 1
    fabricate = True

count = rs.sticky["count"]
