#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import random

# Simulated buoy colors
buoy_colors = ['red', 'green', 'blue']

# Publisher for UAV_cam_task3 and UAV_inspection
uav_cam_task3_pub = None
uav_inspection_pub = None

def publish_uav_cam_task3_and_inspection():
    global uav_cam_task3_pub, uav_inspection_pub
    uav_cam_task3_pub = rospy.Publisher('UAV_cam_task3', String, queue_size=10)
    uav_inspection_pub = rospy.Publisher('UAV_inspection', String, queue_size=10)
    
    rate = rospy.Rate(0.5)  # 2 seconds interval

    while not rospy.is_shutdown():
        # Randomly select a buoy color
        buoy_color = random.choice(buoy_colors)

        # Generate random coordinates
        coordinate_x = round(random.uniform(-10.0, 10.0), 2)
        coordinate_y = round(random.uniform(-10.0, 10.0), 2)
        coordinate_z = round(random.uniform(-10.0, 10.0), 2)

        # Create and publish the UAV_cam_task3 message
        cam_task3_message = "[OBJECT_DETECTED] type={}, distance={}, bearing={}".format(
            buoy_color, coordinate_x, random.uniform(0, 360)
        )
        uav_cam_task3_pub.publish(cam_task3_message)
        rospy.loginfo(f"Published to UAV_cam_task3: {cam_task3_message}")

        # Create and publish the UAV_inspection message
        inspection_message = "{}_buoy: {}, {}, {}".format(
            buoy_color, coordinate_x, coordinate_y, coordinate_z
        )
        uav_inspection_pub.publish(inspection_message)
        rospy.loginfo(f"Published to UAV_inspection: {inspection_message}")

        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('uav_object_detection_publisher')

    try:
        publish_uav_cam_task3_and_inspection()
    except rospy.ROSInterruptException:
        pass
