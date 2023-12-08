#!/usr/bin/env python
import math
import rospy
import random
from std_msgs.msg import Float32
from std_msgs.msg import String

# Global variables to store the color received and the ROS publishers
current_color = ''
speed_publisher = None

# Assume g is 9.81 m/s^2
g = 9.81
# Launch angle in radians
theta = math.radians(30)
# Offsets between the camera and ball launcher
x_offset = 1.0  # horizontal offset in meters
y_offset = 0.5  # vertical offset in meters

# Function to calculate the initial launch speed
def calculate_launch_speed(x, y):
    # Adjust x and y based on the offset
    x += x_offset
    y -= y_offset  # subtract if launcher is higher than the camera

    # Calculate the initial velocity needed to reach the target
    v0_x = math.sqrt(g * x * x / (2 * math.cos(theta) ** 2 * (y + math.tan(theta) * x)))
    v0 = v0_x / math.cos(theta)
    return v0

# Callback function for the 'which_color' subscriber
def which_color_callback(msg):
    global current_color
    current_color = msg.data
    rospy.loginfo(f"Received color: {current_color}")

# Function to scan the specified color and publish the result
def scan_color():
    global current_color, speed_publisher
    # Publisher for 'cam_task7' topic
    pub = rospy.Publisher('cam_task7', String, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        if current_color:
            rospy.loginfo(f"[CAM_TASK7] Scanning {current_color}")
            pub.publish(f"[CAM_TASK7] Scanning {current_color}")

            # Simulated hole distance (x, y, z)
            x_distance = random.uniform(0.5, 5.0)
            y_distance = random.uniform(0.5, 5.0)
            z_distance = random.uniform(0.5, 5.0)  # Not used in calculation, but could be if needed

            # Calculate the launch speed
            launch_speed = calculate_launch_speed(x_distance, y_distance)
            
            # Publish the finding and launch speed
            finding_msg = f"[CAM_TASK7] {current_color.capitalize()} found, hole distance is {x_distance},{y_distance},{z_distance}"
            rospy.loginfo(finding_msg)
            pub.publish(finding_msg)

            speed_msg = Float32()
            speed_msg.data = launch_speed
            speed_publisher.publish(speed_msg)
            rospy.loginfo(f"Published launch speed: {launch_speed}")

            current_color = ''  # Reset color to avoid repetitive processing
        
        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('cam_task7_node', anonymous=True)
        rospy.Subscriber('which_color', String, which_color_callback)
        speed_publisher = rospy.Publisher('ball_launcher_speed', Float32, queue_size=10)
        scan_color()
    except rospy.ROSInterruptException:
        pass
