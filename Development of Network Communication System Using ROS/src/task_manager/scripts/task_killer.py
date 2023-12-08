#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import subprocess

# Dictionary mapping task numbers to their node names
task_nodes = {
    "1": [

    ],
    "2": ["/task2/task2_node",
          "/task2/cam_task2",
          "/task2/ASV_gps",
          "/task2/path_task2",
          "/task2/beacon_detector"
    ],
    "3": ["/task3/task3_node",
          "/task3/cam_task3",
          "/task3/ASV_gps",
          "/task3/path_task3",
          "/task3/UAV_cam_task3",
          "/task3/UAV_gps",
          "/task3/UAV_task3_pp",
    ],
    "4": ["/task4/task4_node",
          "/task4/cam_task4",
          "/task4/ASV_gps",
          "/task4/path_task4",
          "/task4/UAV_cam_task4",
          "/task4/UAV_gps",
          "/task4/UAV_task4_pp",
    ],
    "5": ["/task5/task5_node",
          "/task5/cam_task5"
    ],
    "6": ["/task6/task6_node",
          "/task6/cam_task6",
          "/task6/path_task6"
    ],
    "7": ["/task7/task7_node",
          "/task7/cam_task7"
    ],
    "8": ["/task8/task8_node", 
          "/task8/tin_locator", 
          "/task8/UAV_status", 
          "/task8/UAV_task8_path_planning"
    ],
    "9": ["/task9/task9_node",
          "/task9/RN_locator",
          "/task9/UAV_task9_path_planning",
          "/task9/UAV_gps"
    ]
    # Add other task numbers and node names here
}

def kill_nodes_for_task(task_number):
    if task_number in task_nodes:
        for node_name in task_nodes[task_number]:
            try:
                subprocess.check_call(["rosnode", "kill", node_name])
                rospy.loginfo("Node {} has been killed.".format(node_name))
            except subprocess.CalledProcessError as e:
                rospy.logerr("Failed to kill node {}: {}".format(node_name, str(e)))

def task_to_kill_callback(msg):
    rospy.loginfo("Received a request to kill task: {}".format(msg.data))
    kill_nodes_for_task(msg.data)

def task_killer():
    rospy.init_node('task_killer', anonymous=False)
    rospy.Subscriber('task_to_kill', String, task_to_kill_callback)
    rospy.spin()

if __name__ == '__main__':
    task_killer()
