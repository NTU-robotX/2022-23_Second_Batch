#!/usr/bin/env python
import rospy
import re
from std_msgs.msg import String

# This is a simplified example and does not include all fields.
# You should expand this according to all fields required by your application.

# Global variables to store the latest data
latest_gps_data = None
latest_locator_data = None

# Callback function for the UAV_gps topic
def uav_gps_callback(data):
    global latest_gps_data
    # Assuming the incoming data is a string with comma-separated GPS data
    latest_gps_data = data.data.split(',')

# Callback function for the UAV_cam_RN_locator topic
def uav_cam_rn_locator_callback(data):
    global latest_locator_data
    # Parse the incoming data to extract object distance and detected item
    matches = re.match(r"\[UAV_CAM_RN_LOCATOR\] Object distance: \((.*),(.*),(.*)\), Object (\w) detected", data.data)
    if matches:
        latest_locator_data = {
            'x': float(matches.group(1)),
            'y': float(matches.group(2)),
            'z': float(matches.group(3)),
            'item': matches.group(4)
        }

# Function to format the search and report message
def format_search_report_message(gps_data, locator_data):
    # Extract data and format the message according to the provided example
    # Add all necessary checks and data conversions as required
    message_id = "$RXSAR"
    date = gps_data[1]
    time = gps_data[2]
    object_reported = locator_data['item']
    latitude = gps_data[4]
    ns_indicator = gps_data[5]
    longitude = gps_data[6]
    ew_indicator = gps_data[7]
    team_id = "ROBOT"
    uav_status = "2"  # Assuming UAV is always in 'Autonomous' mode for this example
    checksum = "0D"  # This should be calculated based on the actual message

    # Construct the message string
    message = f"{message_id},{date},{time},{object_reported},{latitude},{ns_indicator},{longitude},{ew_indicator},{object_reported},{latitude},{ns_indicator},{longitude},{ew_indicator},{team_id},{uav_status}*{checksum}"
    return message

def search_and_report_publisher():
    rospy.init_node('uav_search_and_report_publisher', anonymous=True)

    rospy.Subscriber('UAV_gps', String, uav_gps_callback)
    rospy.Subscriber('UAV_cam_RN_locator', String, uav_cam_rn_locator_callback)

    report_publisher = rospy.Publisher('UAV_search_and_report', String, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        if latest_gps_data and latest_locator_data:
            report_message = format_search_report_message(latest_gps_data, latest_locator_data)
            rospy.loginfo(rospy.get_caller_id() + ' [TASK 9 MANAGER] subs %s', report_message)
            report_publisher.publish(String(report_message))

        rate.sleep()

if __name__ == '__main__':
    try:
        search_and_report_publisher()
    except rospy.ROSInterruptException:
        pass
