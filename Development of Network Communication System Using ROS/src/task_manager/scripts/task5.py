#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from datetime import datetime

# This node listens to 'cam_task5' topic for color sequences or 'done'
# Once 'done' is received or every three color sequences, it publishes to 'scan_the_code' topic and then shuts down

# Global variable to keep track of the color sequence
color_sequence = ''

# Callback function for the 'cam_task5' topic
def cam_task5_callback(msg):
    global color_sequence
    # Check if the message is 'done'
    print ("msg:", msg.data)
    if msg.data.lower() == 'done':
        # When 'done' is received, publish to 'scan_the_code' if there is a color sequence
        if color_sequence:
            publish_to_scan_the_code(color_sequence)
        # Shutdown the node
        rospy.signal_shutdown("Completion message received.")
    else:
        # If it's not 'done', it should be a color sequence
        # Append the received color to the sequence
        color_sequence += msg.data[0].upper()
        # Check if we have received three colors
        if len(color_sequence) == 3:
            # Publish the sequence and reset it
            publish_to_scan_the_code(color_sequence)
            color_sequence = ''

# Function to publish to the 'scan_the_code' topic
def publish_to_scan_the_code(sequence):
    # Create the message
    current_time = datetime.now()
    aedt_date = current_time.strftime("%d%m%y")
    aedt_time = current_time.strftime("%H%M%S")
    team_id = "ROBOT"
    checksum = "5E"  # Placeholder checksum, calculate as needed
    formatted_message = f"$RXCOD,{aedt_date},{aedt_time},{team_id},{sequence}*{checksum}"

    # Publish the message
    scan_the_code_publisher.publish(formatted_message)
    rospy.loginfo(f"Published to scan_the_code: {formatted_message}")

# Initialize the ROS node
rospy.init_node('scan_the_code_publisher_node', anonymous=True)

# Create a subscriber for the 'cam_task5' topic
rospy.Subscriber('cam_task5', String, cam_task5_callback)

# Create a publisher for the 'scan_the_code' topic
scan_the_code_publisher = rospy.Publisher('scan_the_code', String, queue_size=10)

# Keep the node running
rospy.spin()
