#!/usr/bin/env python
import rospy
import random
from std_msgs.msg import String

# List of possible colors for the beacons
beacon_colors = ['red', 'green', 'blue']

# Function to generate random beacon data
def generate_beacon_data():
    color = random.choice(beacon_colors)
    distance_x = round(random.uniform(0, 10), 2)  # Random distance in the x-axis
    distance_y = round(random.uniform(0, 10), 2)  # Random distance in the y-axis
    return color, distance_x, distance_y

# Function to publish beacon data
def publish_beacon_data():
    pub = rospy.Publisher('cam_task2', String, queue_size=10)
    rate = rospy.Rate(0.5)  # Set a rate of 2 seconds between messages

    while not rospy.is_shutdown():
        # Generate random beacon data
        color, distance_x, distance_y = generate_beacon_data()

        # Construct and publish the message
        beacon_message = f"{color}: x={distance_x}, y={distance_y}"
        pub.publish(beacon_message)
        rospy.loginfo(f"Published to cam_task2: {beacon_message}")

        rate.sleep()

if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('cam_task2_publisher', anonymous=True)

        # Call the function to publish beacon data
        publish_beacon_data()
    except rospy.ROSInterruptException:
        pass
