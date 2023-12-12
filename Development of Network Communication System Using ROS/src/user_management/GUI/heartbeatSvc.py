import rospy
from std_msgs.msg import String
from your_package_name.msg import Heartbeat  # replace 'your_package_name' with the name of your ROS package
import time

def handle_hb_service():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker')
    rate = rospy.Rate(1)  # 1hz
    while not rospy.is_shutdown():
        hello_str = heartbeat()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

def hb_server():
    rospy.init_node('hb_server')
    s = rospy.Service('heartbeat', Heartbeat, handle_hb_service)
    print('Starting Heartbeat Service')
    rospy.spin()

def heartbeat():
    # Use a breakpoint in the code line below to debug your script.
    msgDate = time.strftime("%d%m%y")  # following RobotX 2023 format ddmmyy
    msgTime = time.strftime("%H%M%S")  # following RobotX 2023 format hhmmss
    msgLat = '21.31198'  # Current Latitude in Decimal degrees
    msgNS = 'N'  # N-North, S-South
    msgLon = '157.88972'  # Current Longitude in Decimal degrees
    msgEW = 'W'  # East/West
    msgTeamID = 'SINGABOAT'
    msgSysMode = '2'  # 1- remote op 2 - autonomous 3- killed
    msgUAVStat = '1'  # 1-stowed 2-deploy 3-fault
    full_message = ('$RXHRB,%s,%s,%s,%s,%s,%s,%s,%s,%s*11' % (
        msgDate, msgTime, msgLat, msgNS, msgLon, msgEW, msgTeamID, msgSysMode, msgUAVStat))
    return full_message

if __name__ == "__main__":
    hb_server()

# def talker():
#     pub = rospy.Publisher('chatter', String, queue_size=10)
#     rospy.init_node('talker', anonymous=True)
#     rate = rospy.Rate(1)  # 1hz
#     while not rospy.is_shutdown():
#         hello_str = heartbeat()
#         rospy.loginfo(hello_str)
#         pub.publish(hello_str)
#         rate.sleep()