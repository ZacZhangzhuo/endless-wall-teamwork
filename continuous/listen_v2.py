import simple_comm as comm

if listen:
    chunks = comm.listen_to_robot("192.168.10.10")
    config = chunks["actual_joints"]