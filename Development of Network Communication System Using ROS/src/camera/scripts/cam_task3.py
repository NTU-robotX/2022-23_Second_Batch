#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import random

# Initialize the ROS node
rospy.init_node('cam_task3_publisher')

# Define the publisher for UAV_cam_task3
cam_task3_pub = rospy.Publisher('cam_task3', String, queue_size=10)

# Define the rate at which to publish messages
rate = rospy.Rate(0.5)  # 2 seconds interval

# Possible objects that can be detected
detected_objects = ['buoy']

# Possible colors for detected objects
colors = ['red', 'green', 'white']

# Main publishing function
def publish_detection():
    while not rospy.is_shutdown():
        # Randomly select an object and color
        detected_object = random.choice(detected_objects)
        color = random.choice(colors)

        # Simulate detection and distance measurement
        distance = round(random.uniform(1.0, 100.0), 2)  # Random distance between 1.0 to 100.0

        # Create and publish the message
        message = f"{detected_object},{color},{distance}"
        cam_task3_pub.publish(message)
        rospy.loginfo(f"Published to cam_task3: {message}")

        # Wait for the defined interval
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_detection()
    except rospy.ROSInterruptException:
        pass
