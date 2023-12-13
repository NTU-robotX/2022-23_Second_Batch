#! /usr/bin/python3
import rospy
from bondpy import bondpy

def formed():
    print("We got a bond")

def broken():
    print("SOMEONE DIED")

rospy.init_node("A", anonymous=True)
b = bondpy.Bond("heartbeat_topic_name","bond_name", on_broken=broken, on_formed=formed)
b.start()
if not b.wait_until_formed():
    raise Exception('Bond could not be formed')
rospy.spin()
# import rospy
# from bondpy import bondpy
# def broken():
#     print('Bond broken')
# def init_bond():
#     id = 'bond123'
#     # Sends id to B using an action or a service
#     bond = bondpy.Bond('hb_bond_topic', 'hb_bond',on_broken=broken())
#     bond.start()
#     print('Starting Bond')
#     if not bond.wait_until_formed(rospy.Duration(10.0)):
#         raise Exception('Bond could not be formed')
#     print('Bond Formed')
# if __name__ == "__main__":
#     rospy.init_node("bond_node", anonymous=True)
#     init_bond()
#     rospy.spin()