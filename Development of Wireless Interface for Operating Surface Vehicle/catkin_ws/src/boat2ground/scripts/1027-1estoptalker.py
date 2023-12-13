#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

import rospy, time
from std_msgs.msg import UInt16
current ='0'
estop_dir='/home/illyas/catkin_ws/src/boat2ground/scripts/estop.txt'
def init():
    pub = rospy.Publisher('toggle_led', UInt16, queue_size=10)
    pub.publish(1)
    rate = rospy.Rate(1)
    rate.sleep()
    pub.publish(0)
    rate.sleep()
    pub.publish(1)
    rate.sleep()
def loop():
    global current
    while not rospy.is_shutdown():
        with open(estop_dir, 'r') as f:
            line = f.readline()
            line = int(line)
            if current != line:
                current = line
                pub = rospy.Publisher('toggle_led', UInt16, queue_size=10)
                rospy.loginfo(line)
                pub.publish(line)
        rate = rospy.Rate(1)  # 1hz
        rate.sleep()

if __name__ == '__main__':
    try:
      rospy.init_node('ES_talker')
      print('Init ES Talker')
      init()
      time.sleep(3)
      loop()
    except rospy.ROSInterruptException:
        pass
