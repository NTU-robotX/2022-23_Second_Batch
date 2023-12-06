#!/usr/bin/env python3
"""
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + ' [TASK 8 MANAGER] %s', data.data)

def subscriber():
    # rospy.Subscriber(this_nodes_namespace + 'UAV_status', String, callback)
    rospy.Subscriber('UAV_status', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'subscriber' node so that multiple subscribers can
    # run simultaneously.

    # Initialise the node
    rospy.init_node("task8", anonymous=True)

    # Display the namespace of the node handle
    rospy.loginfo("[SUBSCRIBER PY  NODE] namespace of node = " + rospy.get_namespace())

    # Put the namespace into a global variable for this script
    global this_nodes_namespace
    this_nodes_namespace = rospy.get_namespace()

    subscriber() """

import rospy
from std_msgs.msg import String
from datetime import datetime

def callback_uav_status(data):
    rospy.loginfo(rospy.get_caller_id() + ' [TASK 8 MANAGER] subs %s', data.data)
    
    global UAV_status
    # Parsing the value after [topic]
    UAV_status = data.data.split(":")[1].split(",")[0].strip()
    publish_task8_message()

def callback_tin_status(data):
    rospy.loginfo(rospy.get_caller_id() + ' [TASK 8 MANAGER] subs %s', data.data)
    
    global tin_status
    # Parsing the value to get tin_status
    tin_status = data.data.split(" ")[1].split(",")[0].strip()
    print(f"tin_status: {tin_status}")
    publish_task8_message()

def publish_task8_message():
    if UAV_status and tin_status:
        # Getting the current datetime
        current_time = datetime.now()
        ddmmyy = current_time.strftime("%d%m%y")
        hhmmss = current_time.strftime("%H%M%S")

        # Creating the message
        task8_message = f"$RXUAV,{ddmmyy},{hhmmss},ROBOT,{UAV_status},{tin_status}*2C"
        
        # Publishing the message to the task8_message: UAV_replenishment topic
        task8_pub.publish(task8_message)

def subscriber():
    rospy.Subscriber('UAV_status', String, callback_uav_status)
    rospy.Subscriber('UAV_tin_status', String, callback_tin_status)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    global task8_pub, node_name 
    node_name = "task8"

    # Initialize the node
    rospy.init_node(node_name, anonymous=True)

    # Creating a publisher for the UAV_replenishment topic
    task8_pub = rospy.Publisher('UAV_replenishment', String, queue_size=10)

    # Display the namespace of the node handle
    rospy.loginfo("[TASK 8 MANAGER] namespace of node = " + rospy.get_namespace())

    # Put the namespace into a global variable for this script
    global this_nodes_namespace, UAV_status, tin_status
    this_nodes_namespace = rospy.get_namespace()
    UAV_status = None
    tin_status = None

    subscriber()