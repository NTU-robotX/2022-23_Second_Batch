#!/usr/bin/env python
import rospy
from std_msgs.msg import String

# Global variables to store incoming data
visible_beacon_data = None
beacon_frequency_data = None
asv_gps_data = None

# Callback functions for subscribers
def cam_task2_callback(msg):
    global visible_beacon_data
    visible_beacon_data = msg.data
    rospy.loginfo(f"Received beacon data: {visible_beacon_data}")

def beacon_freq_callback(msg):
    global beacon_frequency_data
    beacon_frequency_data = msg.data
    rospy.loginfo(f"Received beacon frequency: {beacon_frequency_data}")

def asv_gps_callback(msg):
    global asv_gps_data
    asv_gps_data = msg.data
    rospy.loginfo(f"Received ASV GPS data: {asv_gps_data}")

# Function to perform path planning and publish propeller speed and gate information
def perform_path_planning():
    propeller_speed_pub = rospy.Publisher('propeller_speed', String, queue_size=10)
    which_gate_pub = rospy.Publisher('which_gate', String, queue_size=10)

    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        # Perform path planning based on received data
        if visible_beacon_data and beacon_frequency_data and asv_gps_data:
            # Here you should implement the logic to parse your specific message formats
            # and calculate cmd_vel and orientation

            # For demonstration purposes, we'll just create a dummy cmd_vel and orientation
            cmd_vel = "1.0"  # Placeholder for calculated velocity
            orientation = "0.0"  # Placeholder for calculated orientation

            # Publish to propeller_speed topic
            propeller_speed_message = f"[PROPELLER_SPEED] cmd_vel={cmd_vel}, orientation={orientation}"
            propeller_speed_pub.publish(propeller_speed_message)
            rospy.loginfo(f"Published to propeller_speed: {propeller_speed_message}")

            # Placeholder for entrance and exit gate logic
            entrance_gate = "1"  # Placeholder for entrance gate number
            exit_gate = "3"  # Placeholder for exit gate number

            # Publish the entrance and exit gate numbers
            gate_message = f"Entrance Gate: {entrance_gate}, Exit Gate: {exit_gate}"
            which_gate_pub.publish(gate_message)
            rospy.loginfo(f"Published to which_gate: {gate_message}")

        rate.sleep()

# Initialize the ROS node
rospy.init_node('asv_path_planning_node', anonymous=True)

# Subscribers for the required topics
rospy.Subscriber('cam_task2', String, cam_task2_callback)
rospy.Subscriber('beacon_freq', String, beacon_freq_callback)
rospy.Subscriber('ASV_gps', String, asv_gps_callback)

# Call the path planning function within the ROS spin loop to ensure it runs continuously
try:
    perform_path_planning()
except rospy.ROSInterruptException:
    pass
