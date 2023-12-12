import rospy
import time
from std_msgs.msg import String

# def ping_node(node_name):
#   """Pings a ROS node and measures the delay."""
#   start_time = time.time()
#   rospy.wait_for_message(node_name, None)
#   end_time = time.time()
#   delay = end_time - start_time
#   print("The delay to ping the node {} is {} seconds.".format(node_name, delay))
def test():
  print('ping check!')
def ping_node():
  start_time = time.time()
  try:
    rospy.wait_for_message('chatter', String,timeout=10)
  except:
    delay = -1
    return delay
  end_time = time.time()
  delay = end_time - start_time
  delay = round(delay,1)
  return delay
if __name__ == "__main__":
  node_name = "/ping"
  rospy.init_node('listener', anonymous=True)
  ping_node(node_name)