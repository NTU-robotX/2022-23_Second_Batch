#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from datetime import datetime
import re

# Initialize global variables to store wildlife classifications
wildlife_detected = []

# This function will generate a checksum for the message
# Here we simply return a placeholder value; you would need to implement your own checksum logic

# This callback function processes messages received on UAV_inspection
def uav_inspection_callback(msg):
    global wildlife_detected
    rospy.loginfo(f"Received on UAV_inspection: {msg.data}")
    
    # Extract the animal classification from the message using regex
    match = re.match(r'(\w+):', msg.data)
    if match:
        wildlife_class = match.group(1)[0].upper()  # Get the first letter and convert to uppercase
        wildlife_detected.append(wildlife_class)

        # If three animals have been detected, publish the message
        if len(wildlife_detected) == 3:
            publish_encounter_message()
            wildlife_detected = []  # Reset the list after publishing

def publish_encounter_message():
    current_time = datetime.now()
    aedt_date = current_time.strftime("%d%m%y")
    aedt_time = current_time.strftime("%H%M%S")

    # Construct the message
    message_content = f"$RXENC,{aedt_date},{aedt_time},ROBOT,{len(wildlife_detected)}"
    for animal in wildlife_detected:
        message_content += f",{animal}"

    full_message = f"{message_content}*51"

    # Publish the message
    encounter_pub.publish(full_message)
    rospy.loginfo(f"Published to wildlife_encounter: {full_message}")

# Initialize the ROS node
rospy.init_node('wildlife_encounter_node')

# Create a subscriber for the 'UAV_inspection' topic
uav_inspection_sub = rospy.Subscriber('UAV_inspection', String, uav_inspection_callback)

# Create a publisher for the 'wildlife_encounter' topic
encounter_pub = rospy.Publisher('wildlife_encounter', String, queue_size=10)

# Keep the node running
rospy.spin()
