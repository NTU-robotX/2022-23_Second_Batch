#!/usr/bin/env python3
import rospy
from task_manager.srv import ManageTask8
import subprocess

task8_process = None

def handle_manage_task8(req):
    global task8_process
    if req.command == "start":
        if task8_process is None:
            task8_process = subprocess.Popen(["python", "task8.py"])
            return True, "Task 8 started."
        else:
            return False, "Task 8 already running."
    elif req.command == "stop":
        if task8_process is not None:
            task8_process.terminate()
            task8_process = None
            return True, "Task 8 stopped."
        else:
            return False, "Task 8 is not running."
    else:
        return False, "Unknown command."

if __name__ == "__main__":
    rospy.init_node('task8_manager')
    s = rospy.Service('manage_task8', ManageTask8, handle_manage_task8)
    rospy.spin()
