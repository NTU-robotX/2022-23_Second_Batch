#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import time

def generate_gps_data():
    """
    Simulate generation of GPS data.
    Replace this with actual data acquisition from your GPS device.
    """
    # Get current time in AEDT (Australian Eastern Daylight Time)
    # You would use your actual GPS device's data here
    current_time = time.gmtime()  # Use time.localtime() if AEDT is your local timezone

    # Format the date and time as ddmmyy and hhmmss
    aedt_date = time.strftime("%d%m%y", current_time)
    aedt_time = time.strftime("%H%M%S", current_time)

    # Simulated GPS coordinates
    latitude = "21.31198"
    longitude = "157.88972"
    ns_indicator = "N"
    ew_indicator = "W"

    # Simulated object being reported (R for Robot, N for None)
    object_reported = "R"

    # Other fields
    team_id = "ROBOT"
    asv_status = "2"  # Assuming Autonomous mode

    # You would include your method of calculating the checksum
    checksum = "0D"

    return f"$ASVGPSDATA,{aedt_date},{aedt_time},{object_reported},{latitude},{ns_indicator},{longitude},{ew_indicator},{object_reported},{latitude},{ns_indicator},{longitude},{ew_indicator},{team_id},{asv_status}*{checksum}"

def publish_gps_data():
    rospy.init_node('asv_gps_publisher', anonymous=True)
    gps_publisher = rospy.Publisher('ASV_gps', String, queue_size=10)

    rate = rospy.Rate(1)  # Adjust the rate as needed for your application

    while not rospy.is_shutdown():
        gps_data = generate_gps_data()
        rospy.loginfo(gps_data)
        gps_publisher.publish(String(gps_data))
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_gps_data()
    except rospy.ROSInterruptException:
        pass
