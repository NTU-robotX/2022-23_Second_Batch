#!/usr/bin/env python3
import rospy,time
checking_nodes = True
is_node_running = False
while checking_nodes:
    rosnode_dynamically_loaded = __import__('rosnode')
    is_node_running = rosnode_dynamically_loaded.rosnode_ping(
            'listener', 1)
    time.sleep(1)
    if is_node_running == False:
    # TODO: Needs to be indicated on GUI
    #      (eg. PluginContainerWidget)
    #     rospy.logerr(e.message)
        is_node_running = False
        checking_nodes = False
        print('Node not running')
        exit()