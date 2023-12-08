#!/usr/bin/env python
import rospy
import random
from std_msgs.msg import String

# Define the animals and their coordinates
animals = {
    'platypus': (2.0, 2.0, 3.0),
    'turtle': (1.5, 2.5, 3.5),
    'crocodile': (1.0, 2.0, 3.0)
}

# Shuffle the animals to randomize the order
animal_keys = list(animals.keys())
random.shuffle(animal_keys)

# Initialize the ROS node
rospy.init_node('uav_animal_publisher')

# Define the publishers
inspection_pub = rospy.Publisher('UAV_inspection', String, queue_size=10)
cam_task_pub = rospy.Publisher('UAV_cam_task4', String, queue_size=10)

rate = rospy.Rate(0.5)  # Set a rate of 2 seconds

# Function to simulate the UAV inspection process
def uav_inspect(animal, coordinates):
    # Simulate object detection
    cam_task_pub.publish(f"Detecting animal at distance {random.uniform(1.0,5.0)},{random.uniform(1.0,5.0)},{random.uniform(1.0,5.0)}")
    rospy.loginfo(f"UAV_cam_task4: Detecting animal")
    rospy.sleep(2)  # Simulate time delay for detection

    # Simulate the UAV approaching the object
    cam_task_pub.publish(f"Approaching animal at distance {random.uniform(1.0,5.0)},{random.uniform(1.0,5.0)},{random.uniform(1.0,5.0)}")
    rospy.loginfo(f"UAV_cam_task4: Approaching animal")
    rospy.sleep(2)  # Simulate time delay for approaching

    # Publish the identified animal to the UAV_inspection topic
    cam_task_pub.publish(f"Animal detected, {animal}")
    inspection_pub.publish(f"{animal}: {coordinates[0]},{coordinates[1]},{coordinates[2]}")
    rospy.loginfo(f"UAV_inspection: {animal} at {coordinates}")

# Main loop
try:
    while not rospy.is_shutdown():
        for animal in animal_keys:
            uav_inspect(animal, animals[animal])
            rate.sleep()

except rospy.ROSInterruptException:
    pass
