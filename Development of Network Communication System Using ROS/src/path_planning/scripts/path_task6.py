#!/usr/bin/env python
import rospy
from std_msgs.msg import String

# Global variables to store the distance and GPS data
dock_distance = {'x': 0, 'y': 0, 'z': 0}
asv_gps = {'latitude': 0, 'longitude': 0}

# Function to parse distance information from the message
def parse_distance(message):
    # Expected format: "[DISTANCE_TO_DOCK] x=1.0, y=2.0, z=3.0 for color red"
    parts = message.replace('[DISTANCE_TO_DOCK]', '').strip().split(',')
    distance = {}
    for part in parts:
        if '=' in part:
            key, value = part.split('=')
            distance[key.strip()] = float(value.split()[0])
    return distance

# Callback function for the 'distance_to_dock' topic
def distance_to_dock_callback(msg):
    global dock_distance
    dock_distance = parse_distance(msg.data)
    rospy.loginfo(f"Distance to dock: {dock_distance}")

    # Logic for checking if near docking station and publishing status
    if is_near_docking_station(dock_distance['x']):
        AMS_status_publisher.publish("completed")
        cmd_vel_publisher.publish("[PROPELLER_SPEED] cmd_vel=0, orientation=0")  # Assuming orientation 0 means stop
        rospy.loginfo("Docking completed")
    else:
        AMS_status_publisher.publish("docking")
        cmd_vel, orientation = path_planning(dock_distance)
        cmd_vel_publisher.publish(f"[PROPELLER_SPEED] cmd_vel={cmd_vel}, orientation={orientation}")
        rospy.loginfo(f"Docking in progress: cmd_vel={cmd_vel}, orientation={orientation}")

# Callback function for the 'ASV_gps' topic
def asv_gps_callback(msg):
    global asv_gps
    # Assuming the GPS message is a string in the format "lat=xx.xxxx, lon=yy.yyyy"
    parts = msg.data.split(',')
    asv_gps = {'latitude': float(parts[0].split('=')[1]), 'longitude': float(parts[1].split('=')[1])}
    rospy.loginfo(f"ASV GPS received: {asv_gps}")

# Function to check if the ASV is near the docking station
def is_near_docking_station(distance_x):
    # Implement the logic to determine if the ASV is near the docking station
    # Placeholder logic: checks if x distance is below a threshold
    threshold = 0.05  # meters, for example
    return distance_x < threshold

def path_planning(distance):
    # Placeholder path planning logic
    # Update the ASV's speed and orientation based on the distance to the docking station
    cmd_vel = "1.0"  # Placeholder speed
    orientation = "0"  # Placeholder orientation

    # Logic to adjust cmd_vel and orientation based on distance can be implemented here

    return cmd_vel, orientation

# Initialize the ROS node
rospy.init_node('path_task6_node', anonymous=True)

# Create a subscriber for the 'distance_to_dock' topic
rospy.Subscriber('distance_to_dock', String, distance_to_dock_callback)

# Create a subscriber for the 'ASV_gps' topic
rospy.Subscriber('ASV_gps', String, asv_gps_callback)

# Create publishers for the 'AMS_status' and 'propeller_speed' topics
AMS_status_publisher = rospy.Publisher('AMS_status', String, queue_size=10)
cmd_vel_publisher = rospy.Publisher('propeller_speed', String, queue_size=10)

# Keep the node running
rospy.spin()



'''
# The placeholder below uses Twist type geometry_msg, 
# this will be easier to use if move_base is used or another navigation stack provided by ROS
# If path planning is derived conventionally, using String (code above) would be easier to use
# since it means only basic calculation is done hence
# the number only need to be sliced from the string data

#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

# Placeholder for the distance to the docking station
dock_distance = None

# Callback function for the 'distance_to_dock' topic
def distance_to_dock_callback(msg):
    global dock_distance
    dock_distance = msg
    rospy.loginfo(f"Distance to dock: {dock_distance}")

    # Check if we are close enough to start docking
    if is_near_docking_station(dock_distance):
        AMS_status_publisher.publish("docking")
        # Send command to adjust orientation and velocity
        cmd_vel = Twist()
        cmd_vel.linear.x = 0.5  # Placeholder linear velocity
        cmd_vel.angular.z = 0.3  # Placeholder angular velocity
        cmd_vel_publisher.publish(cmd_vel)
        rospy.loginfo(f"cmd_vel published: {cmd_vel}")
    else:
        # Continue path planning and send updated cmd_vel
        # ... (Path planning logic goes here)
        pass

# Function to check if the ASV is near the docking station
def is_near_docking_station(distance):
    # Implement the logic to determine if the ASV is near the docking station
    # Placeholder logic: checks if distance is below a threshold
    threshold = 1.0  # meters, for example
    return distance < threshold

# Initialize the ROS node
rospy.init_node('path_task6_node', anonymous=True)

# Create a subscriber for the 'distance_to_dock' topic
rospy.Subscriber('distance_to_dock', Twist, distance_to_dock_callback)

# Create publishers for the 'AMS_status' and 'cmd_vel' topics
AMS_status_publisher = rospy.Publisher('AMS_status', String, queue_size=10)
cmd_vel_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)

# Keep the node running
rospy.spin()

'''