#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from datetime import datetime

# Global variable to store the color once detected
detected_color = None

def calculate_checksum(msg):
    # For simplicity, we'll assume the checksum is a dummy fixed value
    # Replace this with actual checksum calculation if required
    return "40"

def cam_task7_callback(msg):
    global detected_color
    rospy.loginfo(f"Received on cam_task7: {msg.data}")
    current_time = datetime.now()
    aedt_date = current_time.strftime("%d%m%y")
    aedt_time = current_time.strftime("%H%M%S")

    if 'Scanning' in msg.data:
        # Extract the color that is being scanned    
        detected_color = msg.data.split()[-1][0].upper()
        AMS_status = "1" #Scanning
    elif 'found' in msg.data and detected_color:
        # When a color is found, publish to Find_and_Fling with the detected color
        AMS_status = "2" #Flinging
        # Reset the detected color
        # detected_color = None
        
    # Construct the message with the detected color
    message = f"$RXFLG,{aedt_date},{aedt_time},ROBOT,{detected_color},{AMS_status}*{calculate_checksum(msg.data)}"
    
    # Publish the message
    find_and_fling_pub.publish(message)
    rospy.loginfo(f"Published to Find_and_Fling: {message}")
    

# Initialize the ROS node
rospy.init_node('task7_node', anonymous=True)

# Create a subscriber for the 'cam_task7' topic
rospy.Subscriber('cam_task7', String, cam_task7_callback)

# Create a publisher for the 'Find_and_Fling' topic
find_and_fling_pub = rospy.Publisher('Find_and_Fling', String, queue_size=10)

# Keep the node running
rospy.spin()
