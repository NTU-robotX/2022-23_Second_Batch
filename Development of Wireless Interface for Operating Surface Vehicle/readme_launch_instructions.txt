LAUNCH INSTRUCTIONS
Read the ROS guide at wiki.ros.org for basic info.
A.FILE DIRECTORY
Place catkin_ws into your /home directory. You can place the RoboX folder in an accessible location.
B.CONFIGURATION
1. Ensure that Raspberry Pi (MOBC) and Operator Laptop (OCS) are both connected to TP-      Link_F498. MOBC must be connected via LAN to the router itself (yellow cable to yellow port) ,  or through the Ubiquiti Antennas. The OCS can be connected to the router via Wi-Fi or LAN. The Wi-Fi password can be found on the bottom of the router.
2. Ensure all required packages are installed. Ensure you are running Ubuntu 20.04, NOT any newer version (ROS1 Noetic only runs on 20.04). Follow the setup instructions in the ROS Installation Guide at https://wiki.ros.org/ROS/Tutorials
3. Ensure that MOBC is powered on. You can power the MOBC using the USBC cable or the DC port. The MOBC is a Raspberry Pi 4 Model B.
C. LAUNCH
 1. Open a terminal window on the OCS.
 2. ssh into the MOBC. Run the command: ssh illyas-rpi@ubuntu-pi-server 
 The username is illyas-rpi, and the password is s20-30rpi
 3. You should now be in the MOBC terminal. Run the command: roscore
 ROS Master will now start. Open a new terminal window on the OCS.
 4. Run the command: roslaunch boat2ground main.launch
The nodes will now be launched.
 5. Open the RobotX Folder and into the main robotx directory (where the main.py file is located). Open a terminal in this directory and run the command: python main.py
 The GUI should now launch. Click on ENTER, then 'Start Task 1'.
 6. Click on 'Connect Robot' to connect to the MOBC.
