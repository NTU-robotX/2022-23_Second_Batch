#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def publisher():
    # pub = rospy.Publisher(this_nodes_namespace + topic, String, queue_size=10)
    pub = rospy.Publisher(topic, String, queue_size=10)
    
    rate = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
        UAV_status_str = f"[{topic}]: 0, UAV is Stowed, timestamp: {rospy.get_time()}"
        # UAV_status_str = f"[{topic}]: 1, UAV is Deployed, timestamp: {rospy.get_time()}"
        # UAV_status_str = f"[{topic}]: 2, UAV is Faulted, timestamp: {rospy.get_time()}"
        rospy.loginfo(UAV_status_str)
        pub.publish(UAV_status_str)
        rate.sleep()
        

if __name__ == '__main__':
    try:
        global topic, this_nodes_namespace
        topic = 'UAV_status'

        # Initialise the node
        rospy.init_node(topic, anonymous=True)

        # Display the namespace of the node handle
        rospy.loginfo( f"[{topic}] namespace of node = " + rospy.get_namespace())

        # Put the namespace into a global variable for this script
        this_nodes_namespace = rospy.get_namespace()
        

        publisher()
    except rospy.ROSInterruptException:
        pass
