#!/usr/bin/env python

""" import rospy
from std_msgs.msg import String

def publisher():
    pub = rospy.Publisher(topic, String, queue_size=10)
    rate = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
        UAV_mode_str = "0, UAV is in Autonomous Mode %s" % rospy.get_time()
        # UAV_mode_str = "1, UAV is in Manual Mode" % rospy.get_time()\
        rospy.loginfo(UAV_mode_str)
        pub.publish(UAV_mode_str)
        rate.sleep()
    
if __name__ == '__main__':
    try:
        global topic, this_nodes_namespace
        topic = 'UAV_mode'
        # Initialise the node
        rospy.init_node(topic, anonymous=True)

        # Display the namespace of the node handle
        rospy.loginfo( f"[{topic}] namespace of node = " + rospy.get_namespace())

        # Put the namespace into a global variable for this script
        this_nodes_namespace = rospy.get_namespace()

        publisher()
    except rospy.ROSInterruptException:
        pass """

import rospy
from std_msgs.msg import String

def publisher():
    UAV_mode_pub = rospy.Publisher(this_nodes_namespace + 'UAV_mode', String, queue_size=10)
    task_status_pub = rospy.Publisher(this_nodes_namespace + 'task_status', String, queue_size=10)
    rate = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
        UAV_mode_str = "[UAV_MODE] 0, UAV is in Autonomous Mode"
        # UAV_mode_str = "[UAV_MODE] 1, UAV is in Manual Mode"
        
        task_status_str = f"[TASK_STATUS] {task}, Task {task}: {task_details[str(task)]}"
        
        rospy.loginfo(UAV_mode_str)
        UAV_mode_pub.publish(UAV_mode_str)
        
        rospy.loginfo(task_status_str)
        task_status_pub.publish(task_status_str)
        
        rate.sleep()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " received: %s", data.data)
    # Run bash script here to print message to screen
    # print(data.data)
    with open("print_message.sh", "w") as f:
        f.write(f'#!/bin/bash\n')
        f.write(f'echo "\\{data.data}"\n')
    rospy.loginfo("Executing bash script to print message to screen")
    import subprocess
    subprocess.call(["bash", "print_message.sh"])

def subscriber(task):
    if task <= 9:
        if task == 8:
            rospy.Subscriber('UAV_replenishment' , String, callback)
        else:
            rospy.Subscriber('UAV_status', String, callback)

if __name__ == '__main__':
    try:
        global this_nodes_namespace, task, node_name
        node_name = 'GUI'
        
        task_details = {
            "0": "No task, sending heartbeat message",
            "1": "Situational Awareness and Reporting",
            "2": "Entrance and Exit Gates",
            "3": "Follow the Path",
            "4": "Wildlife Encounter – React and Report",
            "5": "Scan the Code",
            "6": "Detect and Dock",
            "7": "Find and Fling",
            "8": "UAV Replenishment",
            "9": "UAV Search and Report"
        }
        
        # Initialise the node
        rospy.init_node(node_name, anonymous=True)

        # Display the namespace of the node handle
        rospy.loginfo(f"[{node_name}] namespace of node = " + rospy.get_namespace())

        # Put the namespace into a global variable for this script
        this_nodes_namespace = rospy.get_namespace()

        task = 8  # Set your task number here
        subscriber(task)
        publisher()

    except rospy.ROSInterruptException:
        pass