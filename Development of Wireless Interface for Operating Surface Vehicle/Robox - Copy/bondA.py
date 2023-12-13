#! /usr/bin/python

import rospy
from bondpy import bondpy

def formed():
    print("We got a bond")

def broken():
    print("SOMEONE DIED")
    exit()

# rospy.init_node("bond_A", anonymous=True)
b = bondpy.Bond("bond_topic","bond_A")
b.start()
if not b.wait_until_formed(rospy.Duration(5.0)):
    raise Exception('Bond could not be formed')
print('Bond formed')
rospy.spin()