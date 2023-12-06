#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import os
import subprocess
import roslaunch


current_task = None
task_launch = None

def callback(data):
    global current_task, task_launch

    rospy.loginfo("[TASK_CHECKER] subs to topic task_status: %s", data.data)
    
    try:
        task_number = int(data.data.split(" ")[1].replace(",", ""))
        if 0 <= task_number <= 9:

            # Stop the previous task if it's different from the current one
            if task_number != current_task:
                if task_launch is not None:
                    task_launch.shutdown()

                # Update current task
                current_task = task_number

                # Launch new task
                uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
                roslaunch.configure_logging(uuid)
                launch_file_path = f"project_launch_files/launch/task{current_task}.launch"
                task_launch = roslaunch.parent.ROSLaunchParent(uuid, [launch_file_path])
                task_launch.start()
                
        else:
            rospy.loginfo(f"Invalid task number: {task_number}")
    except (ValueError, IndexError) as e:
        rospy.loginfo(f"Error in extracting task number: {str(e)}")