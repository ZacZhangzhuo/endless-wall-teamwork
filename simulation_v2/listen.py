
import simple_comm as comm
from compas_fab.robots import Configuration

reload(comm)

if listen:
    chunks = comm.listen_to_robot("192.168.10.10")
    config = chunks["actual_joints"]
    pose = chunks["pose"] 
# configuration = config
# configuration = Configuration.from_revolute_values(config[0],config[1],config[2],config[3],config[4],config[5])
