import sys,subprocess
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
# sys.path.insert(0, '/mnt/c/Users/hp/Desktop/catkin_ws/src')
import images_rc,cv2, time #modules
import rospy,rosnode #ros modules
from std_msgs.msg import String
import listener,pingCheck #user modules
import pingCheck
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QTimer, QThread, pyqtSignal

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from task2_ui import Ui_MainWindow as Ui_Task2
from task3_ui import Ui_MainWindow as Ui_Task3
from task4_ui import Ui_MainWindow as Ui_Task4
from task5_ui import Ui_MainWindow as Ui_Task5
from task6_ui import Ui_MainWindow as Ui_Task6
from task7_ui import Ui_MainWindow as Ui_Task7
from task8_ui import Ui_MainWindow as Ui_Task8
from task9_ui import Ui_MainWindow as Ui_Task9

pages = {}

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def run(self):
        # Initialize the CvBridge
        self.bridge = CvBridge()
        rospy.init_node('video_stream_node', anonymous=True)
        # Subscribe to the image topic
        rospy.Subscriber('/camera/image_raw', Image, self.callback)
        # Start the ROS loop
        rospy.spin()

    def callback(self, data):
        # Convert the ROS image to an OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        # Convert the OpenCV image to QImage
        qt_image = self.convert_cv_qt(cv_image)
        # Emit the signal
        self.change_pixmap_signal.emit(qt_image)

    @staticmethod
    def convert_cv_qt(cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

class MainWindow(QMainWindow):
    def __init__(self):
        with open('estop.txt', 'w') as f:
            f.write('NORM')
        super(MainWindow, self).__init__()
        loadUi("main_gui.ui", self)
        self.pushButton.clicked.connect(self.gototasks)
    
    def gototasks(self):
        screen2_tasks = Screen2_Tasks()
        widget.addWidget(screen2_tasks)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Screen2_Tasks(QMainWindow):
    def __init__(self):
        super(Screen2_Tasks, self).__init__()
        loadUi("page2_tasks.ui", self)
        # self.pushButton.clicked.connect(self.gototask1)
        # self.pushButton_task8.clicked.connect(self.gototask8)
        # self.pushButton_task9.clicked.connect(self.gototask9)

        self.pushButton.clicked.connect(lambda: self.goto_task(Task_1))
        self.pushButton_task2.clicked.connect(lambda: self.goto_task(Task_2))
        self.pushButton_task3.clicked.connect(lambda: self.goto_task(Task_3))
        self.pushButton_task4.clicked.connect(lambda: self.goto_task(Task_4))
        self.pushButton_task5.clicked.connect(lambda: self.goto_task(Task_5))
        self.pushButton_task6.clicked.connect(lambda: self.goto_task(Task_6))
        self.pushButton_task7.clicked.connect(lambda: self.goto_task(Task_7))
        self.pushButton_task8.clicked.connect(lambda: self.goto_task(Task_8))
        self.pushButton_task9.clicked.connect(lambda: self.goto_task(Task_9))
    
    def goto_task(self, task_class):
        if task_class not in pages:
            pages[task_class] = task_class()
            widget.addWidget(pages[task_class])
        widget.setCurrentIndex(widget.indexOf(pages[task_class]))
    
    # def gototask1(self):
    #     task_1 = Task_1()
    #     widget.addWidget(task_1)
    #     widget.setCurrentIndex(widget.currentIndex()+1)
    
    # def gototask8(self):
    #     print("Going to Task 8")
    #     task_8 = Task_8()
    #     widget.addWidget(task_8)
    #     widget.setCurrentIndex(widget.currentIndex()+1)

    # def gototask9(self):
    #     print("Going to Task 9")
    #     task_9 = Task_9()
    #     widget.addWidget(task_9)
    #     widget.setCurrentIndex(widget.currentIndex()+1)

class Task_1(QMainWindow):
    def __init__(self):
        super(Task_1, self).__init__()
        loadUi("task1.ui", self)
        self.buttonBox_6.clicked.connect(self.connectrobot)
        self.buttonBox_5.clicked.connect(self.pinger)
        self.eStopButton.clicked.connect(self.estop)
        self.buttonBox_4.accepted.connect(self.start_cam_1)
        self.buttonBox_4.rejected.connect(self.stop_cam_1)
        self.tableWidget.setColumnWidth(0,250)
        self.backButton.clicked.connect(self.go_back)
    def connectrobot(self):
        self.hb_output.append('Connecting to robot...')
        rospy.init_node('listener')
        self.subscriber = rospy.Subscriber('chatter', String, self.update_label)
        self.hb_output.append('Listener Node Loaded. Waiting for Talker Node.')
    def pinger(self):
        self.hb_output.append('Pinging Talker Node.')
        delay = pingCheck.ping_node()
        if delay == -1:
            delaymsg = 'The robot was disconnected.'
            self.hb_output.append(delaymsg)
        delay = str(delay)
        delaymsg = "The delay to ping the node {} is {} seconds.".format('chatter', delay)
        delayBtn = 'Ping Robot (Last ping: {} seconds)'.format(delay)
        self.buttonBox_5.setText(delayBtn)
        self.hb_output.append(delaymsg)
    def update_label(self, msg):
        logtext= msg.data
        # print(logtext)
        self.hb_output.append(logtext)
        verScrollBar = self.hb_output.verticalScrollBar()
        # print('vsb',verScrollBar.maximum(),'vsb value',verScrollBar.value())
        # scrollIsAtEnd = verScrollBar.maximum() - verScrollBar.value() <=100
        if verScrollBar.maximum() != verScrollBar.value():
            verScrollBar.setValue(verScrollBar.maximum())
        logList = list(logtext.split(","))
        for item in logList:
            self.tableWidget.setItem(logList.index(item)-2,1,QtWidgets.QTableWidgetItem(item))
        # print(logList)
    def estop(self): #NOTE: run estoptalker.py before starting main
        if self.eStopButton.isChecked():
            msg = 'EMERGENCY STOP!!!'
            #EStop Operations
            with open('estop.txt','w') as f:
                f.write('ESTOP')
        else:
            msg = 'NORMAL OPERATION'
            #Normal Operations
            with open('estop.txt','w') as f:
                f.write('NORM')
        print(msg)
        self.hb_output.append(msg)
        return



    def show_frame(self):
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True & cam_on:
                # self.displayImage(label_3, 1)
                frame = cv2.flip(frame, 180)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (395, 260))

                image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                self.label_3.setPixmap(QPixmap.fromImage(image))
                self.label_5.setPixmap(QPixmap.fromImage(image))
                self.label_6.setPixmap(QPixmap.fromImage(image))
                self.label_4.setPixmap(QPixmap.fromImage(image))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
    
    def start_cam_1(self):
        global cam_on, cap
        cam_on = True
        cap = cv2.VideoCapture(0) 
        self.show_frame()
        print("Camera ON")

    def stop_cam_1(self):
        global cam_on
        cam_on = False
        if cap:
            cap.release()
        print("Camera OFF")

class Task_2(QMainWindow):
    update_output_signal = pyqtSignal(str)

    def __init__(self):
        super(Task_2, self).__init__()
        self.ui = Ui_Task2()
        self.ui.setupUi(self)
        self.update_output_signal.connect(self.update_output_box)

        # Add any signals and slots here
        # ROS Publisher
        self.status_publisher = rospy.Publisher('/task_status', String, queue_size=10)
        self.kill_publisher = rospy.Publisher('/task_to_kill', String, queue_size=10)

        # Subscribe to the follow_the_path topic
        rospy.Subscriber('task2/entrance_exit_gate', String, self.entrance_exit_gate_callback)
        
        # Connecting buttons
        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.startButton.clicked.connect(self.start_task)
        self.ui.stopButton.clicked.connect(self.stop_task)

    def go_back(self):
        # Assuming 'widget' is the QStackedWidget instance you are using for your application
        # widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(widget.indexOf(pages[Screen2_Tasks]))

    def start_task(self):
        self.ui.hb_output.append("Starting Task 2...")
        task_msg = String()
        task_msg.data = "[TASK_STATUS] 2, Task 2: Entrance and Exit Gates"
        self.status_publisher.publish(task_msg)
        rospy.loginfo("Published task status update.")

    def stop_task(self):
        kill_msg = String()
        kill_msg.data = "2"
        self.kill_publisher.publish(kill_msg)
        rospy.loginfo("Published task kill command.")
        self.ui.hb_output.append("Task 2 terminated")
    
    def entrance_exit_gate_callback(self, msg):
        # This callback function gets called whenever a new message is received on the 'UAV_replenishment' topic
        # self.update_output_box(msg.data)
        self.update_output_signal.emit(msg.data)
        self.parse_and_update_table(msg.data)

    def update_output_box(self, message_content):
        # Assuming you have a QTextEdit or similar widget in your UI named outputBox
        self.ui.hb_output.append(message_content)  # Update the output box with the raw message

    def parse_and_update_table(self, message_content):     
        # Split the message_content string into parts based on your message format
        # $RXGAT,111221,161229,ROBOT,1,2*3C
        parts = message_content.split(',')
        # print("parts", parts)
        
        # You might want to implement checksum verification here

        # Extracting parts of the message based on the provided table
        message_id = parts[0]  # This is "$RXGAT"
        aedt_date = parts[1]  # This is "111221"
        aedt_time = parts[2]  # This is "161229"
        team_id = parts[3]    # This is "ROBOT"
        entrance = parts[4]    # This is "1"
        exit = parts[5][0]    # This is "2"

        # Update the table with the interpreted values
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{parts[0+1][:2]}-{parts[0+1][2:4]}-{parts[0+1][4:]}"))
        self.ui.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem(f"{parts[1+1][:2]}:{parts[1+1][2:4]}:{parts[1+1][4:]}"))
        self.ui.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem(parts[2+1]))
        self.ui.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem(f"Gate {parts[3+1]}"))
        self.ui.tableWidget.setItem(4, 0, QtWidgets.QTableWidgetItem(f"Gate {parts[4+1][0]}"))

class Task_3(QMainWindow):
    update_output_signal = pyqtSignal(str)

    def __init__(self):
        super(Task_3, self).__init__()
        self.ui = Ui_Task3()
        self.ui.setupUi(self)
        self.update_output_signal.connect(self.update_output_box)

        # Add any signals and slots here
        # ROS Publisher
        self.status_publisher = rospy.Publisher('/task_status', String, queue_size=10)
        self.kill_publisher = rospy.Publisher('/task_to_kill', String, queue_size=10)

        # Subscribe to the follow_the_path topic
        rospy.Subscriber('task3/follow_the_path', String, self.follow_the_path_callback)
        
        # Connecting buttons
        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.startButton.clicked.connect(self.start_task)
        self.ui.stopButton.clicked.connect(self.stop_task)

    def go_back(self):
        # Assuming 'widget' is the QStackedWidget instance you are using for your application
        # widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(widget.indexOf(pages[Screen2_Tasks]))

    def start_task(self):
        self.ui.hb_output.append("Starting Task 3...")
        task_msg = String()
        task_msg.data = "[TASK_STATUS] 3, Task 3: Follow the Path"
        self.status_publisher.publish(task_msg)
        rospy.loginfo("Published task status update.")

    def stop_task(self):
        kill_msg = String()
        kill_msg.data = "3"
        self.kill_publisher.publish(kill_msg)
        rospy.loginfo("Published task kill command.")
        self.ui.hb_output.append("Task 3 terminated")
    
    def follow_the_path_callback(self, msg):
        # This callback function gets called whenever a new message is received on the 'UAV_replenishment' topic
        # self.update_output_box(msg.data)
        self.update_output_signal.emit(msg.data)
        self.parse_and_update_table(msg.data)

    def update_output_box(self, message_content):
        # Assuming you have a QTextEdit or similar widget in your UI named outputBox
        self.ui.hb_output.append(message_content)  # Update the output box with the raw message

    def parse_and_update_table(self, message_content):     
        # Split the message_content string into parts based on your message format
        # $RXPTH,111221,161229,ROBOT,1*3C
        parts = message_content.split(',')
        # print("parts", parts)
        
        # You might want to implement checksum verification here

        # Extracting parts of the message based on the provided table
        message_id = parts[0]  # This is "$RXPTH"
        aedt_date = parts[1]  # This is "111221"
        aedt_time = parts[2]  # This is "161229"
        team_id = parts[3]    # This is "ROBOT"
        finished = parts[4][0]    # This is "1"

        # Map the status codes to their meanings
        progress_map = {
            "1": "In Progress",
            "2": "Completed"
        }

        # Update the table with the interpreted values
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{parts[0+1][:2]}-{parts[0+1][2:4]}-{parts[0+1][4:]}"))
        self.ui.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem(f"{parts[1+1][:2]}:{parts[1+1][2:4]}:{parts[1+1][4:]}"))
        self.ui.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem(parts[2+1]))
        self.ui.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem(progress_map[parts[3+1][0]]))

class Task_4(QMainWindow):
    update_output_signal = pyqtSignal(str)

    def __init__(self):
        super(Task_4, self).__init__()
        self.ui = Ui_Task4()
        self.ui.setupUi(self)
        self.update_output_signal.connect(self.update_output_box)

        # Add any signals and slots here
        # ROS Publisher
        self.status_publisher = rospy.Publisher('/task_status', String, queue_size=10)
        self.kill_publisher = rospy.Publisher('/task_to_kill', String, queue_size=10)

        # Subscribe to the wildlife_encounter topic
        rospy.Subscriber('task4/wildlife_encounter', String, self.wildlife_encounter_callback)
        
        # Connecting buttons
        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.startButton.clicked.connect(self.start_task)
        self.ui.stopButton.clicked.connect(self.stop_task)

    def go_back(self):
        # Assuming 'widget' is the QStackedWidget instance you are using for your application
        # widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(widget.indexOf(pages[Screen2_Tasks]))

    def start_task(self):
        self.ui.hb_output.append("Starting Task 4...")
        task_msg = String()
        task_msg.data = "[TASK_STATUS] 4, Task 4: Wildlife Encounter - React and Report"
        self.status_publisher.publish(task_msg)
        rospy.loginfo("Published task status update.")

    def stop_task(self):
        kill_msg = String()
        kill_msg.data = "4"
        self.kill_publisher.publish(kill_msg)
        rospy.loginfo("Published task kill command.")
        self.ui.hb_output.append("Task 4 terminated")
    
    def wildlife_encounter_callback(self, msg):
        # This callback function gets called whenever a new message is received on the 'UAV_replenishment' topic
        # self.update_output_box(msg.data)
        self.update_output_signal.emit(msg.data)
        self.parse_and_update_table(msg.data)

    def update_output_box(self, message_content):
        # Assuming you have a QTextEdit or similar widget in your UI named outputBox
        self.ui.hb_output.append(message_content)  # Update the output box with the raw message

    def parse_and_update_table(self, message_content):     
        # Split the message_content string into parts based on your message format
        # $RXENC,111221,161229,ROBOT,3,P,C,T*51
        parts = message_content.split(',')
        # print("parts", parts)
        
        # You might want to implement checksum verification here

        # Extracting parts of the message based on the provided table
        message_id = parts[0]  # This is "$RXENC"
        aedt_date = parts[1]  # This is "111221"
        aedt_time = parts[2]  # This is "161229"
        team_id = parts[3]    # This is "ROBOT"
        obj_total = parts[4]    # This is "3"
        obj1 = parts[5]    # This is "P"
        obj2 = parts[6]    # This is "C"
        obj3 = parts[7][0] # This is "T"

        # Map the status codes to their meanings
        animal_map = {
            "P": "Platypus",
            "C": "Crocodile",
            "T": "Turtle"
        }

        # Update the table with the interpreted values
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{parts[0+1][:2]}-{parts[0+1][2:4]}-{parts[0+1][4:]}"))
        self.ui.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem(f"{parts[1+1][:2]}:{parts[1+1][2:4]}:{parts[1+1][4:]}"))
        self.ui.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem(parts[2+1]))
        self.ui.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem(parts[3+1]))
        self.ui.tableWidget.setItem(4, 0, QtWidgets.QTableWidgetItem(animal_map[parts[4+1]]))
        self.ui.tableWidget.setItem(5, 0, QtWidgets.QTableWidgetItem(animal_map[parts[5+1]]))
        self.ui.tableWidget.setItem(6, 0, QtWidgets.QTableWidgetItem(animal_map[parts[6+1][0]]))

class Task_5(QMainWindow):
    update_output_signal = pyqtSignal(str)

    def __init__(self):
        super(Task_5, self).__init__()
        self.ui = Ui_Task5()
        self.ui.setupUi(self)
        self.initialize_table()
        self.update_output_signal.connect(self.update_output_box)
        
        # Add any signals and slots here
        # ROS Publisher
        self.status_publisher = rospy.Publisher('/task_status', String, queue_size=10)
        self.kill_publisher = rospy.Publisher('/task_to_kill', String, queue_size=10)

        # Subscribe to the scan_the_code topic
        rospy.Subscriber('task5/scan_the_code', String, self.scan_the_code)
        
        # Connecting buttons
        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.startButton.clicked.connect(self.start_task)
        self.ui.stopButton.clicked.connect(self.stop_task)

        # Create the video thread
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)

        # Start the thread
        self.thread.start()

    @pyqtSlot(QImage)
    def update_image(self, qt_image):
        # If camera_box is the QLabel object where you want to display the image
        self.ui.camera_box.setPixmap(qt_image)

    def initialize_table(self):
        # Define your keys here
        keys = ["Date ", "Time", "Team ID ", "Light Pattern"]
        
        # Set the row count to match the number of keys
        self.ui.tableWidget.setRowCount(len(keys))
        
        # Initialize the first column with the keys
        for i, key in enumerate(keys):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(key))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(""))  # Initialize with empty value


    def go_back(self):
        # widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(widget.indexOf(pages[Screen2_Tasks]))

    def start_task(self):
        self.ui.hb_output.append("Starting Task 5...")
        task_msg = String()
        task_msg.data = "[TASK_STATUS] 5, Task 5: Scan the Code"
        self.status_publisher.publish(task_msg)
        rospy.loginfo("Published task status update.")

    def stop_task(self):
        kill_msg = String()
        kill_msg.data = "5"
        self.kill_publisher.publish(kill_msg)
        rospy.loginfo("Published task kill command.")
        self.ui.hb_output.append("Task 5 terminated")
    
    def scan_the_code(self, msg):
        # This callback function gets called whenever a new message is received on the 'UAV_replenishment' topic
        # self.update_output_box(msg.data)
        self.update_output_signal.emit(msg.data)
        self.parse_and_update_table(msg.data)

    def update_output_box(self, message_content):
        # Assuming you have a QTextEdit or similar widget in your UI named outputBox
        self.ui.hb_output.append(message_content)  # Update the output box with the raw message

    def parse_and_update_table(self, message_content):     
        # Split the message_content string into parts based on your message format
        # $RXCOD,111221,161229,ROBOT,RBG*5E
        parts = message_content.split(',')
        # print("parts", parts)
        
        # You might want to implement checksum verification here

        # Extracting parts of the message based on the provided table
        message_id = parts[0]  # This is "$RXCOD"
        aedt_date = parts[1]  # This is "111221"
        aedt_time = parts[2]  # This is "161229"
        team_id = parts[3]    # This is "ROBOT"
        light_seq = parts[4][:3] # This is "RBG"

        # Map the status codes to their meanings
        color_map = {
            "R": "Red ",
            "B": "Blue ",
            "G": "Green "
        }

        # Update the table with the interpreted values
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{parts[0+1][:2]}-{parts[0+1][2:4]}-{parts[0+1][4:]}"))
        self.ui.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem(f"{parts[1+1][:2]}:{parts[1+1][2:4]}:{parts[1+1][4:]}"))
        self.ui.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem(parts[2+1]))

        print ("light_seq", light_seq)
        temp = ''
        for letter in light_seq:
            temp += color_map[letter]
        self.ui.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem(temp))

    def update_table(self, key, value):
        # Find the row with the specified key and update its value
        for row in range(self.ui.tableWidget.rowCount()):
            cell_item = self.ui.tableWidget.item(row, 0)  # Get the item in the first column (key column)
            if cell_item is not None and cell_item.text() == key:
                # Update the value in the second column
                self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(value))
                return  # Exit the function once the update is done

        # If the key was not found, then there's a problem with table initialization
        print(f"Key {key} not found in the table")

class Task_6(QMainWindow):
    update_output_signal = pyqtSignal(str)

    def __init__(self):
        super(Task_6, self).__init__()
        self.ui = Ui_Task6()
        self.ui.setupUi(self)
        self.initialize_table()
        self.update_output_signal.connect(self.update_output_box)
        
        # Add any signals and slots here
        # ROS Publisher
        self.status_publisher = rospy.Publisher('/task_status', String, queue_size=10)
        self.kill_publisher = rospy.Publisher('/task_to_kill', String, queue_size=10)
        self.color_publisher = rospy.Publisher('/task6/which_color', String, queue_size=10)

        # Subscribe to the detect_and_dock topic
        rospy.Subscriber('task6/detect_and_dock', String, self.detect_and_dock)
        
        # Connecting buttons
        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.startButton.clicked.connect(self.start_task)
        self.ui.stopButton.clicked.connect(self.stop_task)

        self.ui.redButton_2.clicked.connect(lambda: self.publish_color('red'))
        self.ui.greenButton_2.clicked.connect(lambda: self.publish_color('green'))
        self.ui.blueButton_2.clicked.connect(lambda: self.publish_color('blue'))

    def publish_color(self, color):
        self.color_publisher.publish(color)
        rospy.loginfo(f"Published color: {color}")
        self.ui.hb_output.append("Waiting for the next color...")

    def initialize_table(self):
        # Define your keys here
        keys = ["Date ", "Time", "Team ID ", "Color", "AMS Status"]
        
        # Set the row count to match the number of keys
        self.ui.tableWidget.setRowCount(len(keys))
        
        # Initialize the first column with the keys
        for i, key in enumerate(keys):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(key))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(""))  # Initialize with empty value


    def go_back(self):
        # widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(widget.indexOf(pages[Screen2_Tasks]))

    def start_task(self):
        self.ui.hb_output.append("Starting Task 6...")
        task_msg = String()
        task_msg.data = "[TASK_STATUS] 6, Task 6: Detect and Dock"
        self.status_publisher.publish(task_msg)
        rospy.loginfo("Published task status update.")
        self.ui.hb_output.append("Waiting for which color...")

    def stop_task(self):
        kill_msg = String()
        kill_msg.data = "6"
        self.kill_publisher.publish(kill_msg)
        rospy.loginfo("Published task kill command.")
        self.ui.hb_output.append("Task 6 terminated")
    
    def detect_and_dock(self, msg):
        # This callback function gets called whenever a new message is received on the 'UAV_replenishment' topic
        # self.update_output_box(msg.data)
        self.update_output_signal.emit(msg.data)
        self.parse_and_update_table(msg.data)

    def update_output_box(self, message_content):
        # Assuming you have a QTextEdit or similar widget in your UI named outputBox
        self.ui.hb_output.append(message_content)  # Update the output box with the raw message

    def parse_and_update_table(self, message_content):     
        # Split the message_content string into parts based on your message format
        # Example message format: "$RXDOK,111221,161229,ROBOT,R,2*2C"
        parts = message_content.split(',')
        # print("parts", parts)
        
        # You might want to implement checksum verification here

        # Extracting parts of the message based on the provided table
        message_id = parts[0]  # This is "$RXDOK"
        aedt_date = parts[1]  # This is "111221"
        aedt_time = parts[2]  # This is "161229"
        team_id = parts[3]    # This is "ROBOT"
        color = parts[4] # This is "R"
        ams_status = parts[5][0] # This is "2"

        # Map the status codes to their meanings
        color_map = {
            "R": "Red",
            "G": "Green",
            "B": "Blue"
        }
        ams_status_map = {
            "1": "Docking",
            "2": "Complete"
        }

        # Update the table with the interpreted values
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{parts[0+1][:2]}-{parts[0+1][2:4]}-{parts[0+1][4:]}"))
        self.ui.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem(f"{parts[1+1][:2]}:{parts[1+1][2:4]}:{parts[1+1][4:]}"))
        self.ui.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem(parts[2+1]))
        self.ui.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem(color_map.get(parts[3+1])))
        self.ui.tableWidget.setItem(4, 0, QtWidgets.QTableWidgetItem(ams_status_map.get(parts[4+1][0])))

class Task_7(QMainWindow):
    update_output_signal = pyqtSignal(str)

    def __init__(self):
        super(Task_7, self).__init__()
        self.ui = Ui_Task7()
        self.ui.setupUi(self)
        self.initialize_table()
        self.update_output_signal.connect(self.update_output_box)
        
        # Add any signals and slots here
        # ROS Publisher
        self.status_publisher = rospy.Publisher('/task_status', String, queue_size=10)
        self.kill_publisher = rospy.Publisher('/task_to_kill', String, queue_size=10)
        self.color_publisher = rospy.Publisher('/task7/which_color', String, queue_size=10)

        # Subscribe to the Find_and_Fling topic
        rospy.Subscriber('task7/Find_and_Fling', String, self.find_and_fling)
        
        # Connecting buttons
        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.startButton.clicked.connect(self.start_task)
        self.ui.stopButton.clicked.connect(self.stop_task)

        self.ui.redButton.clicked.connect(lambda: self.publish_color('red'))
        self.ui.greenButton.clicked.connect(lambda: self.publish_color('green'))
        self.ui.blueButton.clicked.connect(lambda: self.publish_color('blue'))

    def publish_color(self, color):
        self.color_publisher.publish(color)
        rospy.loginfo(f"Published color: {color}")
        self.ui.hb_output.append("Waiting for the next color...")

    def initialize_table(self):
        # Define your keys here
        keys = ["Date ", "Time", "Team ID ", "Target Color", "AMS Status"]
        
        # Set the row count to match the number of keys
        self.ui.tableWidget.setRowCount(len(keys))
        
        # Initialize the first column with the keys
        for i, key in enumerate(keys):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(key))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(""))  # Initialize with empty value


    def go_back(self):
        # widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(widget.indexOf(pages[Screen2_Tasks]))

    def start_task(self):
        self.ui.hb_output.append("Starting Task 7...")
        task_msg = String()
        task_msg.data = "[TASK_STATUS] 7, Task 7: Find and Fling"
        self.status_publisher.publish(task_msg)
        rospy.loginfo("Published task status update.")
        self.ui.hb_output.append("Waiting for which color...")

    def stop_task(self):
        kill_msg = String()
        kill_msg.data = "7"
        self.kill_publisher.publish(kill_msg)
        rospy.loginfo("Published task kill command.")
        self.ui.hb_output.append("Task 7 terminated")
    
    def find_and_fling(self, msg):
        # This callback function gets called whenever a new message is received on the 'UAV_replenishment' topic
        # self.update_output_box(msg.data)
        self.update_output_signal.emit(msg.data)
        self.parse_and_update_table(msg.data)

    def update_output_box(self, message_content):
        # Assuming you have a QTextEdit or similar widget in your UI named outputBox
        self.ui.hb_output.append(message_content)  # Update the output box with the raw message

    def parse_and_update_table(self, message_content):     
        # Split the message_content string into parts based on your message format
        # Example message format: "$RXFLG,111221,161229,ROBOT,R,2*2C"
        parts = message_content.split(',')
        # print("parts", parts)
        
        # You might want to implement checksum verification here

        # Extracting parts of the message based on the provided table
        message_id = parts[0]  # This is "$RXFLG"
        aedt_date = parts[1]  # This is "111221"
        aedt_time = parts[2]  # This is "161229"
        team_id = parts[3]    # This is "ROBOT"
        color = parts[4] # This is "R"
        ams_status = parts[5][0] # This is "2"

        # Map the status codes to their meanings
        color_map = {
            "R": "Red",
            "G": "Green",
            "B": "Blue"
        }
        ams_status_map = {
            "1": "Scanning",
            "2": "Flinging"
        }

        # Update the table with the interpreted values
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{parts[0+1][:2]}-{parts[0+1][2:4]}-{parts[0+1][4:]}"))
        self.ui.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem(f"{parts[1+1][:2]}:{parts[1+1][2:4]}:{parts[1+1][4:]}"))
        self.ui.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem(parts[2+1]))
        self.ui.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem(color_map.get(parts[3+1])))
        self.ui.tableWidget.setItem(4, 0, QtWidgets.QTableWidgetItem(ams_status_map.get(parts[4+1][0])))

class Task_8(QMainWindow):
    update_output_signal = pyqtSignal(str)

    def __init__(self):
        super(Task_8, self).__init__()
        self.ui = Ui_Task8()
        self.ui.setupUi(self)
        self.initialize_table()
        self.update_output_signal.connect(self.update_output_box)
        
        # Add any signals and slots here
        # ROS Publisher
        self.status_publisher = rospy.Publisher('/task_status', String, queue_size=10)
        self.kill_publisher = rospy.Publisher('/task_to_kill', String, queue_size=10)

        # Subscribe to the UAV_replenishment topic
        rospy.Subscriber('task8/UAV_replenishment', String, self.uav_replenishment_callback)
        
        # Connecting buttons
        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.startButton.clicked.connect(self.start_task)
        self.ui.stopButton.clicked.connect(self.stop_task)

    def initialize_table(self):
        # Define your keys here
        keys = ["Date ", "Time", "Team ID ", "UAV Status", "Item Status "]
        
        # Set the row count to match the number of keys
        self.ui.tableWidget.setRowCount(len(keys))
        
        # Initialize the first column with the keys
        for i, key in enumerate(keys):
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(key))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(""))  # Initialize with empty value


    def go_back(self):
        # widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(widget.indexOf(pages[Screen2_Tasks]))

    def start_task(self):
        self.ui.hb_output.append("Starting Task 8...")
        task_msg = String()
        task_msg.data = "[TASK_STATUS] 8, Task 8: UAV Replenishment"
        self.status_publisher.publish(task_msg)
        rospy.loginfo("Published task status update.")

    def stop_task(self):
        kill_msg = String()
        kill_msg.data = "8"
        self.kill_publisher.publish(kill_msg)
        rospy.loginfo("Published task kill command.")
        self.ui.hb_output.append("Task 8 terminated")
    
    def uav_replenishment_callback(self, msg):
        # This callback function gets called whenever a new message is received on the 'UAV_replenishment' topic
        # self.update_output_box(msg.data)
        self.update_output_signal.emit(msg.data)
        self.parse_and_update_table(msg.data)

    def update_output_box(self, message_content):
        # Assuming you have a QTextEdit or similar widget in your UI named outputBox
        self.ui.hb_output.append(message_content)  # Update the output box with the raw message

    def parse_and_update_table(self, message_content):     
        # Split the message_content string into parts based on your message format
        # Example message format: "$RXUAV,111221,161229,ROBOT,1,0*2C"
        parts = message_content.split(',')
        # print("parts", parts)
        
        # You might want to implement checksum verification here

        # Extracting parts of the message based on the provided table
        message_id = parts[0]  # This is "$RXUAV"
        aedt_date = parts[1]  # This is "111221"
        aedt_time = parts[2]  # This is "161229"
        team_id = parts[3]    # This is "ROBOT"
        uav_status = parts[4] # This is "1"
        item_status = parts[5][0] # This is "0"

        # Map the status codes to their meanings
        uav_status_map = {
            "1": "Stowed",
            "2": "Deployed",
            "3": "Faulted"
        }
        item_status_map = {
            "0": "Not Picked Up",
            "1": "Picked Up",
            "2": "Delivered"
        }

        # Update the table with the interpreted values
        self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{parts[0+1][:2]}-{parts[0+1][2:4]}-{parts[0+1][4:]}"))
        self.ui.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem(f"{parts[1+1][:2]}:{parts[1+1][2:4]}:{parts[1+1][4:]}"))
        self.ui.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem(parts[2+1]))
        self.ui.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem(uav_status_map.get(parts[3+1])))
        self.ui.tableWidget.setItem(4, 0, QtWidgets.QTableWidgetItem(item_status_map.get(parts[4+1][0])))
        # self.update_table("Date ", aedt_date)
        # self.update_table("Time", aedt_time)
        # self.update_table("Team ID ", team_id)
        # self.update_table("UAV Status", uav_status_map.get(uav_status, "Unknown"))
        # self.update_table("Item Status ", item_status_map.get(item_status, "Unknown"))

    def update_table(self, key, value):
        # Find the row with the specified key and update its value
        for row in range(self.ui.tableWidget.rowCount()):
            cell_item = self.ui.tableWidget.item(row, 0)  # Get the item in the first column (key column)
            if cell_item is not None and cell_item.text() == key:
                # Update the value in the second column
                self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(value))
                return  # Exit the function once the update is done

        # If the key was not found, then there's a problem with table initialization
        print(f"Key {key} not found in the table")

class Task_9(QMainWindow):
    update_output_signal = pyqtSignal(str)

    def __init__(self):
        super(Task_9, self).__init__()
        self.ui = Ui_Task9()
        self.ui.setupUi(self)
        self.update_output_signal.connect(self.update_output_box)

        # Add any signals and slots here
        # ROS Publisher
        self.status_publisher = rospy.Publisher('/task_status', String, queue_size=10)
        self.kill_publisher = rospy.Publisher('/task_to_kill', String, queue_size=10)

        # Subscribe to the UAV_search_and_rescue topic
        rospy.Subscriber('task9/UAV_search_and_report', String, self.uav_sar_callback)
        
        # Connecting buttons
        self.ui.backButton.clicked.connect(self.go_back)
        self.ui.startButton.clicked.connect(self.start_task)
        self.ui.stopButton.clicked.connect(self.stop_task)

    def go_back(self):
        # Assuming 'widget' is the QStackedWidget instance you are using for your application
        # widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(widget.indexOf(pages[Screen2_Tasks]))

    def start_task(self):
        self.ui.hb_output.append("Starting Task 9...")
        task_msg = String()
        task_msg.data = "[TASK_STATUS] 9, Task 9: UAV Search and Report"
        self.status_publisher.publish(task_msg)
        rospy.loginfo("Published task status update.")

    def stop_task(self):
        kill_msg = String()
        kill_msg.data = "9"
        self.kill_publisher.publish(kill_msg)
        rospy.loginfo("Published task kill command.")
        self.ui.hb_output.append("Task 9 terminated")
    
    def uav_sar_callback(self, msg):
        # This callback function gets called whenever a new message is received on the 'UAV_replenishment' topic
        # self.update_output_box(msg.data)
        self.update_output_signal.emit(msg.data)
        self.parse_and_update_table(msg.data)

    def update_output_box(self, message_content):
        # Assuming you have a QTextEdit or similar widget in your UI named outputBox
        self.ui.hb_output.append(message_content)  # Update the output box with the raw message

    def parse_and_update_table(self, message_content):
        # Assuming message_content is a string like:
        # "$RXSAR,111221,161229,R,21.31198,N,157.88972,W,N,21.32198,N,157.89972,W,ROBOT,2*0D"
        uav_status_map = {
            "1": "Stowed",
            "2": "Deployed",
            "3": "Faulted"
        }

        parts = message_content.split(',')
        # Make sure that parts has enough elements to unpack
        if len(parts) < 13:
            print("Incomplete message for Task 9")
            return
        
        # Unpacking parts to variables
        protocol_header, aedt_date, aedt_time, object_reported, latitude, ns_indicator, longitude, ew_indicator, object_reported2, latitude2, ns_indicator2, longitude2, ew_indicator2, team_id, status_checksum = parts
        
        # Process date and time to correct format
        formatted_date = f"{aedt_date[:2]}-{aedt_date[2:4]}-20{aedt_date[4:]}"
        formatted_time = f"{aedt_time[:2]}:{aedt_time[2:4]}:{aedt_time[4:]}"
        
        # Process team ID and status, splitting the checksum
        status, checksum_part = status_checksum.split('*')

        # Update table directly with the values
        self.update_table(0, "Date", formatted_date)
        self.update_table(1, "Time", formatted_time)
        self.update_table(2, "Object 1", object_reported)
        self.update_table(3, "Object 1 Latitude", latitude)
        self.update_table(4, "Object 1 N/S Indicator", ns_indicator)
        self.update_table(5, "Object 1 Longitude", longitude)
        self.update_table(6, "Object 1 E/W Indicator", ew_indicator)
        self.update_table(7, "Object 2", object_reported2)
        self.update_table(8, "Object 2 Latitude", latitude2)
        self.update_table(9, "Object 2 N/S Indicator", ns_indicator2)
        self.update_table(10, "Object 2 Longitude", longitude2)
        self.update_table(11, "Object 2 E/W Indicator", ew_indicator2)
        self.update_table(12, "Team ID", team_id)
        self.update_table(13, "UAV Status", uav_status_map.get(status, "Unknown"))

    def update_table(self, row, key, value):
        # Directly set the item for the specified row and column
        self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(value))
        # self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(value))

# Main
if __name__ == '__main__':
    rospy.init_node('GUI', anonymous=True)
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    # Store the main window and task selection screen in the pages dictionary
    pages[MainWindow] = MainWindow()
    pages[Screen2_Tasks] = Screen2_Tasks()

    # Add the main window and task selection screen to the widget stack
    widget.addWidget(pages[MainWindow])
    widget.addWidget(pages[Screen2_Tasks])

    # Show the widget stack
    widget.show()

    # Set up the ROS shutdown hook
    app.aboutToQuit.connect(lambda: rospy.signal_shutdown('GUI Shutdown'))

    sys.exit(app.exec_())