#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import random

# Global variables to store UAV GPS and camera task data
uav_gps_data = None
uav_cam_task3_data = None

def uav_gps_callback(msg):
    global uav_gps_data
    # Here, we'll assume that the msg.data is a string formatted as required
    uav_gps_data = msg.data
    rospy.loginfo(f"UAV GPS data: {uav_gps_data}")

def uav_cam_task3_callback(msg):
    global uav_cam_task3_data
    # The msg.data is assumed to be a string containing relevant camera task data
    uav_cam_task3_data = msg.data
    rospy.loginfo(f"UAV Camera Task 3 data: {uav_cam_task3_data}")

def publish_drone_speed():
    drone_speed_pub = rospy.Publisher('drone_speed', String, queue_size=10)
    rate = rospy.Rate(1)  # Adjust the rate as per your requirement

    while not rospy.is_shutdown():
        cmd_vel = random.uniform(0.5, 2.0)  # Random velocity
        orientation = random.uniform(0, 360.0)  # Random orientation

        # Construct the drone speed message
        drone_speed_message = f"[DRONE_SPEED] cmd_vel={cmd_vel}, orientation={orientation}"
        drone_speed_pub.publish(drone_speed_message)
        rospy.loginfo(f"Published to drone_speed: {drone_speed_message}")

        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('uav_path_planning_node')

    rospy.Subscriber('UAV_gps', String, uav_gps_callback)
    rospy.Subscriber('UAV_cam_task3', String, uav_cam_task3_callback)

    try:
        publish_drone_speed()
    except rospy.ROSInterruptException:
        pass
