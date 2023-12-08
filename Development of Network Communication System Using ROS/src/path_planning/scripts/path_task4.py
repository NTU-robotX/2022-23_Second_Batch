#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import re
import random

# Placeholder for current state
current_animal = None
current_coordinates = None
asv_gps_data = None
avoiding_crocodile = False

# Callback functions
def inspection_callback(msg):
    global current_animal, current_coordinates, avoiding_crocodile
    rospy.loginfo(f"Inspection data received: {msg.data}")
    animal, coordinates = msg.data.split(': ')
    current_animal = animal
    current_coordinates = list(map(float, coordinates.split(',')))
    if animal.lower() == 'crocodile':
        avoiding_crocodile = True
    else:
        avoiding_crocodile = False
        approach_animal()

def asv_gps_callback(msg):
    global asv_gps_data
    rospy.loginfo(f"ASV GPS data received: {msg.data}")
    asv_gps_data = msg.data

def cam_task4_callback(msg):
    rospy.loginfo(f"Cam task4 data received: {msg.data}")
    if not avoiding_crocodile:
        # Extract the buoy distance from the message
        match = re.search(r'distance ([\d.]+),([\d.]+),([\d.]+)', msg.data)
        if match:
            distance = list(map(float, match.groups()))
            adjust_approach(distance)

# Function to approach the animal
def approach_animal():
    # This function uses the current_coordinates to issue commands to the ASV
    # to approach the detected animal's location
    cmd_vel, orientation = calculate_movement(current_animal, current_coordinates)
    publish_propeller_speed(cmd_vel, orientation)

# Function to adjust the approach based on cam_task4 data
def adjust_approach(distance):
    # Use the distance to the buoy to fine-tune the ASV's approach
    cmd_vel, orientation = calculate_adjustments(distance)
    publish_propeller_speed(cmd_vel, orientation)

# Path planning functions (placeholders)
def calculate_movement(animal, coordinates):
    # Implement actual movement calculation here
    # Placeholder: randomly set cmd_vel and orientation
    cmd_vel = 1.0  # Example velocity
    orientation = random.uniform(0,360)
    return cmd_vel, orientation

def calculate_adjustments(distance):
    # Implement actual adjustment calculation here
    # Placeholder: set cmd_vel to slow down as we approach the buoy
    cmd_vel = 0.5 if distance[0] < 1.0 else 1.0
    orientation = random.uniform(0,360)
    return cmd_vel, orientation

# Function to publish the propeller speed
def publish_propeller_speed(cmd_vel, orientation):
    # Construct the message
    propeller_speed_msg = f"[PROPELLER_SPEED] cmd_vel={cmd_vel}, orientation={orientation}"
    propeller_speed_pub.publish(propeller_speed_msg)
    rospy.loginfo(f"Propeller speed published: {propeller_speed_msg}")

# Initialize the ROS node
rospy.init_node('asv_path_planning_node')

# Define publishers and subscribers
inspection_sub = rospy.Subscriber('UAV_inspection', String, inspection_callback)
asv_gps_sub = rospy.Subscriber('ASV_gps', String, asv_gps_callback)
cam_task4_sub = rospy.Subscriber('cam_task4', String, cam_task4_callback)
propeller_speed_pub = rospy.Publisher('propeller_speed', String, queue_size=10)

# Main loop
try:
    rospy.spin()
except rospy.ROSInterruptException:
    pass
