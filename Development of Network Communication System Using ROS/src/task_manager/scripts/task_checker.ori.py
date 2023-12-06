#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import os
import subprocess

current_task_process = None
current_task_number = -1

def callback(data):
    global current_task_process, current_task_number

    rospy.loginfo("[TASK_CHECKER] subs to topic task_status: %s", data.data)
    
    # Extracting task number from received message
    try:
        new_task_number = int(data.data.split(" ")[1].replace(",", ""))
        if 0 <= new_task_number <= 9:
            script_name = f"task{new_task_number}.py"

            if new_task_number != current_task_number:
                # If a task is currently running, terminate it before starting a new one
                if current_task_process is not None:
                    current_task_process.terminate()
                    rospy.loginfo(f"Terminated previous task process")

                if os.path.isfile(f"scripts/{script_name}"):
                    rospy.loginfo(f"Executing {script_name}")
                    current_task_process = subprocess.Popen(["python", f"scripts/{script_name}"])
                    current_task_number = new_task_number  # Update the current task number
                else:
                    rospy.loginfo(f"{script_name} does not exist in the directory")
            else:
                rospy.loginfo(f"Task {new_task_number} is already running")
        else:
            rospy.loginfo(f"Invalid task number: {new_task_number}")
    except (ValueError, IndexError) as e:
        rospy.loginfo(f"Error in extracting task number: {str(e)}")

def listener():
    # Initialize the node
    rospy.init_node('task_checker', anonymous=True)
    
    # Subscribe to the 'task_status' topic
    rospy.Subscriber('task_status', String, callback)
    
    # Keep python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
