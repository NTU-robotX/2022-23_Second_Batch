#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import random
import time

# Initialize the ROS node
rospy.init_node('cam_task4_publisher')

# Define the publisher for 'cam_task4'
cam_task4_pub = rospy.Publisher('cam_task4', String, queue_size=10)

# Define a list of objects that the camera might detect

def detect_objects():
    rate = rospy.Rate(1)  # 1 Hz, adjust if needed for your application

    while not rospy.is_shutdown():
        # Randomly choose an object to detect
        detected_object = 'wildlife'

        # Simulate the detection of the object and its distance
        # Here we are just generating some random coordinates for the example
        x = round(random.uniform(1, 10), 2)
        y = round(random.uniform(1, 10), 2)
        z = round(random.uniform(1, 10), 2)

        # Construct the detection message
        detection_message = f"A {detected_object} detected at distance x={x}, y={y}, z={z}"

        # Publish the message to the 'cam_task4' topic
        cam_task4_pub.publish(detection_message)
        rospy.loginfo(f"Published: {detection_message}")

        # Wait for the next cycle
        rate.sleep()

if __name__ == '__main__':
    try:
        detect_objects()
    except rospy.ROSInterruptException:
        pass
