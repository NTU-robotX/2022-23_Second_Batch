#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import subprocess

# Dictionary to map task numbers to the respective launch file commands
# task_launch_files = {
#     "8": "launch/task8.launch"
#     # Add other tasks and their corresponding launch files here
# }

def task_status_callback(msg):
    rospy.loginfo(rospy.get_caller_id() + " I heard %s", msg.data)
    # Extract the task number from the message
    try:
        # Extract task number assuming the message format is correct
        task_number = msg.data.split(' ')[1][0].strip('{}')
        
        # Check if the task number has a corresponding launch file
        if 1 <= int(task_number) <= 9:
            # launch_file = task_launch_files[task_number]
            launch_file = f"task{task_number}.launch"
            
            rospy.loginfo("Launching task number {}: {}".format(task_number, launch_file))
            # Run the roslaunch command for the corresponding task
            subprocess.call(["roslaunch", "project_launch_files", launch_file])
            # task_launch = roslaunch.parent.ROSLaunchParent(uuid, [launch_file])
        else:
            rospy.logwarn("No launch file for task number: {}".format(task_number))
    except IndexError as e:
        rospy.logerr("The message does not have the expected format: {}".format(e))

def task_checker():
    rospy.init_node('task_checker', anonymous=True)
    rospy.Subscriber("task_status", String, task_status_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        task_checker()
    except rospy.ROSInterruptException:
        pass
