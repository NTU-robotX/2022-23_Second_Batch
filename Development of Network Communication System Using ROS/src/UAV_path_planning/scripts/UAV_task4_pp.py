#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from datetime import datetime
import random

# Placeholder for GPS data
uav_gps_data = None
asv_gps_data = None

# Callback functions
def cam_task4_callback(msg):
    rospy.loginfo(f"Cam task4 data received: {msg.data}")
    splitted_msg = msg.data.split()
    if splitted_msg[0]=="Detecting" or splitted_msg[0]=="Approaching":
        # Extract the animal and coordinates
        coordinates = splitted_msg[-1]
        x, y, z = map(float, coordinates.split(','))
        # Perform path planning (placeholder function call)
        plan_path(x, y, z)

def uav_gps_callback(msg):
    global uav_gps_data
    rospy.loginfo(f"UAV GPS data received: {msg.data}")
    uav_gps_data = msg.data

def asv_gps_callback(msg):
    global asv_gps_data
    rospy.loginfo(f"ASV GPS data received: {msg.data}")
    asv_gps_data = msg.data

# Path planning function (placeholder)
def plan_path(x, y, z):
    # Implement actual path planning logic here
    # Placeholder: randomly set cmd_vel and orientation
    cmd_vel = random.uniform(0.5, 2.0)  # Random velocity
    orientation = random.uniform(0.0,360.0)  # Random orientation

    # Publish the drone speed and orientation
    drone_speed_msg = f"[DRONE_SPEED] cmd_vel={cmd_vel}, orientation={orientation}"
    drone_speed_pub.publish(drone_speed_msg)
    rospy.loginfo(f"Drone speed published: {drone_speed_msg}")

# Initialize the ROS node
rospy.init_node('uav_path_planning_node')

# Define publishers and subscribers
inspection_sub = rospy.Subscriber('UAV_cam_task4', String, cam_task4_callback)
uav_gps_sub = rospy.Subscriber('UAV_gps', String, uav_gps_callback)
asv_gps_sub = rospy.Subscriber('ASV_gps', String, asv_gps_callback)
drone_speed_pub = rospy.Publisher('drone_speed', String, queue_size=10)

# Main loop
try:
    rospy.spin()
except rospy.ROSInterruptException:
    pass
