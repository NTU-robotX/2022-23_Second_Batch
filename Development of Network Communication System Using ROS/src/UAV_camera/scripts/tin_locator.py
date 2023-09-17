#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def publisher():
    pub_cam_tin = rospy.Publisher(this_nodes_namespace + 'UAV_cam_tin', String, queue_size=10)
    pub_tin_status = rospy.Publisher(this_nodes_namespace + 'UAV_tin_status', String, queue_size=10)
    
    rate = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
        if task_status == 8:
            # Customize these with your actual coordinates and status
            x, y, z = 1.0, 2.0, 3.0
            item_status = 0
            status_details = ["Not Picked Up", "Picked Up", "Delivered"]

            cam_tin_str = f"[UAV_CAM_TIN] Tin coordinate: ({x},{y},{z})"
            item_status_str = f"[UAV_TIN_STATUS] {item_status}, Tin is {status_details[item_status]}"

            rospy.loginfo(cam_tin_str)
            pub_cam_tin.publish(cam_tin_str)
            
            rospy.loginfo(item_status_str)
            pub_tin_status.publish(item_status_str)
        
        rate.sleep()

def callback(data):
    global task_status
    task_status = int(data.data.split(" ")[1].replace(",", ""))
    rospy.loginfo("Updated task status: %d", task_status)

if __name__ == '__main__':
    try:
        global this_nodes_namespace, node_name, task_status
        node_name = 'tin_locator'
        task_status = -1

        rospy.init_node(node_name, anonymous=True)

        # Put the namespace into a global variable for this script
        this_nodes_namespace = rospy.get_namespace()

        # Subscribing to the 'task_status' topic
        rospy.Subscriber(this_nodes_namespace + 'task_status', String, callback)

        publisher()
    except rospy.ROSInterruptException:
        pass
