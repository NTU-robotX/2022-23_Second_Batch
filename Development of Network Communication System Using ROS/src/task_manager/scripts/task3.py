#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from datetime import datetime

def calculate_checksum(data):
    # Placeholder function for checksum calculation
    # Replace with actual checksum calculation if needed
    return "3C"

def ams_status_callback(msg):
    # Convert the status message to the required finished status code
    finished_status_code = "1" if msg.data == "in progress" else "2"

    # Get the current date and time
    current_time = datetime.now()
    aedt_date = current_time.strftime("%d%m%y")
    aedt_time = current_time.strftime("%H%M%S")

    # Construct the message
    message = f"$RXPTH,{aedt_date},{aedt_time},ROBOT,{finished_status_code}*{calculate_checksum(msg.data)}"

    # Publish the message
    follow_the_path_pub.publish(message)
    rospy.loginfo(f"Published to follow_the_path: {message}")

# Initialize the ROS node
rospy.init_node('task3_node')

# Create a subscriber for the 'AMS_status' topic
rospy.Subscriber('AMS_status', String, ams_status_callback)

# Create a publisher for the 'follow_the_path' topic
follow_the_path_pub = rospy.Publisher('follow_the_path', String, queue_size=10)

# Spin to keep the script for listening to the AMS_status
rospy.spin()
