#!/usr/bin/env python
import rospy
import re
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
import time


# SCENARIO 1. tin distance given
# Global variables to store the last distances and time
last_distances = None
last_time = None

# Updated callback function for UAV_cam_tin topic
def uav_gps_callback(data):
    global latest_gps
    # Parse the incoming data to extract latitude, longitude, altitude
    matches = re.match(r"\[UAV_GPS\] GPS coordinate: \((.*),(.*),(.*)\)", data.data)
    if matches:
        latest_gps = [float(matches.group(i)) for i in range(1, 4)]

def uav_cam_tin_callback(data):
    global last_distances
    # Parse the incoming data to extract dx, dy, dz
    matches = re.match(r"\[UAV_CAM_TIN\] Tin distance: \((.*),(.*),(.*)\)", data.data)
    if matches:
        last_distances = [float(matches.group(i)) for i in range(1, 4)]

# Function to calculate speed based on change in distances
def calculate_speed(current_distances, time_diff):
    if last_distances is None or time_diff == 0:
        return 0, 0, 0  # Avoid division by zero

    ddx = (current_distances[0] - last_distances[0]) / time_diff
    ddy = (current_distances[1] - last_distances[1]) / time_diff
    ddz = (current_distances[2] - last_distances[2]) / time_diff
    return ddx, ddy, ddz

# Inside the main loop of the listener function
def listener():
    global latest_tin, latest_gps, last_time

    rospy.init_node('drone_speed_calculator', anonymous=True)

    rospy.Subscriber('UAV_cam_tin', String, uav_cam_tin_callback)
    # rospy.Subscriber('UAV_gps', String, uav_gps_callback)

    speed_publisher = rospy.Publisher('drone_speed', Vector3, queue_size=10)
    rate = rospy.Rate(10)  # 10hz

    while not rospy.is_shutdown():
        current_time = time.time()
        if last_distances is not None and last_time is not None:
            time_diff = current_time - last_time
            speed = calculate_speed(last_distances, time_diff)
            speed_msg = Vector3(*speed)
            speed_publisher.publish(speed_msg)

        last_time = current_time
        rate.sleep()

''' # SCENARIO 2, tin coordinate given
# Global variables to store the latest data
latest_tin = None
latest_gps = None
last_time = None

# Callback function for UAV_cam_tin topic
def uav_cam_tin_callback(data):
    global latest_tin
    # Parse the incoming data to extract x, y, z
    matches = re.match(r"\[UAV_CAM_TIN\] Tin coordinate: \((.*),(.*),(.*)\)", data.data)
    if matches:
        latest_tin = [float(matches.group(i)) for i in range(1, 4)]

# Callback function for UAV_gps topic
def uav_gps_callback(data):
    global latest_gps
    # Parse the incoming data to extract latitude, longitude, altitude
    matches = re.match(r"\[UAV_GPS\] GPS coordinate: \((.*),(.*),(.*)\)", data.data)
    if matches:
        latest_gps = [float(matches.group(i)) for i in range(1, 4)]

# Function to calculate speed
def calculate_speed(tin, gps, time_diff):
    # Simple distance formula: sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)
    # Divided by time to get speed
    if time_diff == 0:
        return 0, 0, 0  # Avoid division by zero

    dx = (gps[0] - tin[0]) / time_diff
    dy = (gps[1] - tin[1]) / time_diff
    dz = (gps[2] - tin[2]) / time_diff
    return dx, dy, dz

def listener():
    global latest_tin, latest_gps, last_time

    rospy.init_node('drone_speed_calculator', anonymous=True)

    rospy.Subscriber('UAV_cam_tin', String, uav_cam_tin_callback)
    rospy.Subscriber('UAV_gps_simple', String, uav_gps_callback)

    speed_publisher = rospy.Publisher('drone_speed', Vector3, queue_size=10)
    rate = rospy.Rate(10)  # 10hz

    while not rospy.is_shutdown():
        current_time = time.time()
        if latest_tin is not None and latest_gps is not None and last_time is not None:
            time_diff = current_time - last_time
            speed = calculate_speed(latest_tin, latest_gps, time_diff)
            speed_msg = Vector3(*speed)
            speed_publisher.publish(speed_msg)

        last_time = current_time
        rate.sleep()
'''

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
