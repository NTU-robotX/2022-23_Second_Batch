#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Point

# This function is a placeholder for the actual logic that determines
# the distance based on the color.
# This is to be replaced with the actual distance measurement function of the camera
def get_distance_for_color(color):
    # Placeholder values: you should implement the logic to determine these
    # based on the color and your application's needs.
    distances = {
        'red': (0.02, 2.0, 3.0),
        'blue': (4.0, 5.0, 6.0),
        'green': (7.0, 8.0, 9.0)
    }
    return distances.get(color.lower(), (0.0, 0.0, 0.0))

# Callback function for the 'which_color' topic
def which_color_callback(msg):
    color = msg.data
    rospy.loginfo(f"Received color: {color}")

    # Get the x, y, z distances for the color
    distance_x, distance_y, distance_z = get_distance_for_color(color)
    
    # Create a new Point message for the distance
    distance_msg = Point()
    distance_msg.x = distance_x
    distance_msg.y = distance_y
    distance_msg.z = distance_z
    
    # Publish the required distance to the 'distance_to_dock' topic
    distance_publisher.publish(f"[DISTANCE_TO_DOCK] x={distance_x}, y={distance_y}, z={distance_z} for color {color}")
    rospy.loginfo(f"[DISTANCE_TO_DOCK] Published distance to dock: x={distance_x}, y={distance_y}, z={distance_z} for color {color}")

# Initialize the ROS node
rospy.init_node('cam_task6_node', anonymous=True)

# Create a subscriber for the 'which_color' topic
rospy.Subscriber('which_color', String, which_color_callback)

# Create a publisher for the 'distance_to_dock' topic
distance_publisher = rospy.Publisher('distance_to_dock', String, queue_size=10)

# Keep the node running
rospy.spin()
