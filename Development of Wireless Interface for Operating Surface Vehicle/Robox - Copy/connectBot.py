#!/usr/bin/env python3
import rospy
from bondpy import bondpy

def formed():
    print("We got a bond")

def broken():
    print("SOMEONE DIED")

rospy.init_node('A', anonymous=True)
b = bondpy.Bond("chatter","bond_name", on_broken=broken, on_formed=formed)
b.start()
if not b.wait_until_formed():
    raise Exception('Bond could not be formed')

rospy.spin()