#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from datetime import datetime

# Global variables to store the AMS status and the color
ams_status = None
dock_color = None

def ams_status_callback(msg):
    global ams_status
    ams_status = msg.data
    rospy.loginfo(f"Received AMS status: {ams_status}")
    publish_detect_and_dock()

def which_color_callback(msg):
    global dock_color
    dock_color = msg.data
    rospy.loginfo(f"Received docking color: {dock_color}")
    publish_detect_and_dock()

def publish_detect_and_dock():
    if ams_status and dock_color:
        current_time = datetime.now()
        formatted_date = current_time.strftime("%d%m%y")
        formatted_time = current_time.strftime("%H%M%S")

        message_id = "$RXDOK"
        team_id = "ROBOT"
        color = dock_color[0].upper()
        status = "1" if ams_status == "docking" else "2"
        checksum = "4E"  # Placeholder for checksum

        formatted_message = f"{message_id},{formatted_date},{formatted_time},{team_id},{color},{status}*{checksum}"
        detect_and_dock_pub.publish(formatted_message)
        rospy.loginfo(f"Published to detect_and_dock: {formatted_message}")

# Initialize the ROS node
rospy.init_node('task6_node', anonymous=True)

# Create subscribers for the 'AMS_status' and 'which_color' topics
rospy.Subscriber('AMS_status', String, ams_status_callback)
rospy.Subscriber('which_color', String, which_color_callback)

# Create a publisher for the 'detect_and_dock' topic
detect_and_dock_pub = rospy.Publisher('detect_and_dock', String, queue_size=10)

# Keep the node running
rospy.spin()
