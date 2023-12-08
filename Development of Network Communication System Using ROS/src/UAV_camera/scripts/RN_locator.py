#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def publisher():
    pub_cam_RN = rospy.Publisher( 'UAV_cam_RN_locator', String, queue_size=10)
    
    rate = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
        # if task_status == 8:
        x, y, z = 1.0, 2.0, 3.0
        item = "R" # or "N"

        text_str = f"[UAV_CAM_RN_LOCATOR] Object distance: ({x},{y},{z}), Object {item} detected"
        
        rospy.loginfo(text_str)
        pub_cam_RN.publish(text_str)
        
        rate.sleep()

def callback(data):
    global task_status
    task_status = int(data.data.split(" ")[1].replace(",", ""))
    rospy.loginfo("Updated task status: %d", task_status)

if __name__ == '__main__':
    try:
        global this_nodes_namespace, node_name, task_status
        node_name = 'RN_locator'
        task_status = -1

        rospy.init_node(node_name, anonymous=True)

        publisher()
    except rospy.ROSInterruptException:
        pass
