#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import random
import time

def publish_gps_data():
    rospy.init_node('uav_gps_publisher', anonymous=True)
    gps_publisher = rospy.Publisher('UAV_gps', String, queue_size=10)
    rate = rospy.Rate(1)  # Publish at 1 Hz

    while not rospy.is_shutdown():
        # Generate random GPS coordinates for simulation
        latitude = random.uniform(-90.0, 90.0)
        longitude = random.uniform(-180.0, 180.0)
        altitude = random.uniform(0.0, 1000.0)  # Simulating altitude in meters

        # Create the GPS data string
        gps_data = f"[UAV_GPS] GPS coordinate: ({latitude},{longitude},{altitude})"
        rospy.loginfo(gps_data)

        # Publish the GPS data
        gps_publisher.publish(String(gps_data))

        rate.sleep()

if __name__ == '__main__':
    try:
        publish_gps_data()
    except rospy.ROSInterruptException:
        pass
