#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import time

# Simulated sequence of colors to be sent
# This is to be replaced with the actual camera reading
color_sequence = ['red', 'blue', 'green', 'green', 'blue', 'green', 'blue', 'green', 'red']
color_index = 0  # Index of the next color to send
colors_sent = 0  # Counter for colors sent in the current sequence

def send_color_sequence():
    global color_index, colors_sent
    pub = rospy.Publisher('cam_task5', String, queue_size=10)
    rospy.sleep(1)
    rate = rospy.Rate(1)  # 1 Hz (every 1 second)

    while not rospy.is_shutdown() and color_index < len(color_sequence):
        # Send the next color in the sequence
        color = color_sequence[color_index]
        rospy.loginfo(f"Sending color: {color}")
        pub.publish(color)
        colors_sent += 1
        color_index += 1

        # Wait for 1 second
        rate.sleep()

        # Check if 3 colors have been sent, if so, pause for 2 seconds
        if colors_sent == 3:
            rospy.loginfo("Pausing for 2 seconds.")
            time.sleep(2)
            colors_sent = 0  # Reset the counter after the pause

    # If all colors in the sequence have been sent, send 'done'
    # This has to be changed to a function that tries to detect if there is no more color in 2 seconds
    # then it will send 'done'
    if color_index >= len(color_sequence):
        rospy.loginfo("All colors sent. Sending 'done'.")
        pub.publish('done')

if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('cam_task5_node', anonymous=True)

        # Call the function to send the color sequence
        send_color_sequence()
    except rospy.ROSInterruptException:
        pass