#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import random

# Function to publish frequency data
def publish_frequency_data():
    pub = rospy.Publisher('beacon_freq', String, queue_size=10)
    rate = rospy.Rate(1)  # Set a rate of 1 Hz

    while not rospy.is_shutdown():
        # Generate a random frequency value between 1.0 and 5.0
        # You may want to adjust these values according to your needs
        freq = random.uniform(1.0, 5.0)

        # Construct and publish the frequency message
        freq_message = String()
        freq_message.data = str(freq)
        pub.publish(freq_message)
        rospy.loginfo(f"Published to beacon_freq: {freq_message.data}")

        rate.sleep()

if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('beacon_detector', anonymous=True)

        # Call the function to publish frequency data
        publish_frequency_data()
    except rospy.ROSInterruptException:
        pass
