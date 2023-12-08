#!/usr/bin/env python
import rospy
import re
from std_msgs.msg import String
from geometry_msgs.msg import Vector3

# Global variables to store the latest data
latest_gps_data = None
latest_locator_data = None

# Callback function for the UAV_gps topic
def uav_gps_callback(data):
    global latest_gps_data
    # Assuming the incoming data is a string with comma-separated GPS data
    latest_gps_data = data.data.split(',')

# Callback function for the UAV_cam_RN_locator topic
def uav_cam_rn_locator_callback(data):
    global latest_locator_data
    # Parse the incoming data to extract object distance and detected item
    matches = re.match(r"\[UAV_CAM_RN_LOCATOR\] Object distance: \((.*),(.*),(.*)\), Object (\w) detected", data.data)
    if matches:
        latest_locator_data = {
            'x': float(matches.group(1)),
            'y': float(matches.group(2)),
            'z': float(matches.group(3)),
            'item': matches.group(4)
        }

# Function to calculate the drone's speed to arrive at the given R/N item
def calculate_navigation_speed(locator_data, speed_factor=1.0):
    # Speed factor is a constant to adjust the speed, it can be determined based on your drone's capabilities
    # In a real-world scenario, you would also consider the drone's maximum speed and acceleration capabilities
    # Here, we are simply using the relative distances as a proxy for speed
    navigation_speed = Vector3()
    navigation_speed.x = locator_data['x'] * speed_factor
    navigation_speed.y = locator_data['y'] * speed_factor
    navigation_speed.z = locator_data['z'] * speed_factor
    return navigation_speed

def navigation_speed_publisher():
    rospy.init_node('drone_navigation_speed_publisher', anonymous=True)

    rospy.Subscriber('UAV_gps', String, uav_gps_callback)
    rospy.Subscriber('UAV_cam_RN_locator', String, uav_cam_rn_locator_callback)

    speed_publisher = rospy.Publisher('drone_speed', Vector3, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz, adjust as necessary

    while not rospy.is_shutdown():
        if latest_locator_data:
            # Calculate the speed needed to reach the R/N item
            navigation_speed = calculate_navigation_speed(latest_locator_data)
            rospy.loginfo(f"Publishing navigation speed: {navigation_speed}")
            speed_publisher.publish(navigation_speed)

        rate.sleep()

if __name__ == '__main__':
    try:
        navigation_speed_publisher()
    except rospy.ROSInterruptException:
        pass
