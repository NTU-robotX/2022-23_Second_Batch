#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from datetime import datetime

# Function to calculate a simple checksum by summing the ASCII values of the message
def calculate_checksum(message):
    return sum(ord(char) for char in message) % 256

# Callback function for the 'which_gate' topic
def which_gate_callback(msg):
    # Extracting entrance and exit gate information from the message
    gates_info = msg.data.split(',')
    entrance_gate = gates_info[0][-1]
    exit_gate = gates_info[1][-1]

    # Preparing the message to be sent
    current_time = datetime.now()
    aedt_date = current_time.strftime("%d%m%y")
    aedt_time = current_time.strftime("%H%M%S")
    team_id = "ROBOT"  # Assuming the team ID is ROBOT

    # Constructing the message without checksum
    message = f"$RXGAT,{aedt_date},{aedt_time},{team_id},{entrance_gate},{exit_gate}"
    # checksum = calculate_checksum(message)
    # Constructing the complete message with checksum
    complete_message = f"{message}*3C"

    # Publish the message to the 'entrance_exit_gate' topic
    entrance_exit_gate_pub.publish(complete_message)
    rospy.loginfo(f"Published to entrance_exit_gate: {complete_message}")

# Initialize the ROS node
rospy.init_node('gate_publisher_node', anonymous=True)

# Create a publisher for the 'entrance_exit_gate' topic
entrance_exit_gate_pub = rospy.Publisher('entrance_exit_gate', String, queue_size=10)

# Create a subscriber for the 'which_gate' topic
rospy.Subscriber('which_gate', String, which_gate_callback)

# Keep the node running
rospy.spin()
