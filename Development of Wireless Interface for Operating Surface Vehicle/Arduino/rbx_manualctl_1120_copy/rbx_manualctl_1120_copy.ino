# include <ros.h>
# include <std_msgs/String.h>
# include <std_msgs/UInt16.h>

//declare ROS vars

//Future emergency stop button implementation
//Flysky not implemented here 
//# define BUTTON 8 
# define ESS 13 //Emergency Stop Pin

ros::NodeHandle node_handle;
std_msgs::String button_msg;
std_msgs::UInt16 ess_msg;

double Ch1 = 2; //left motor
int MotorL; int MotorR;
double Ch2 = 3; // right motor
int Ch5 = 5; // e-stop SWA
int Ch6 = 7; // auto/manual SWD
int in1 = 4; //L298
int in2 = 8; //L298

bool PWR = true;
// byte estop;
// const byte LED_PIN = 13;

//ROS Subscriber callback
void subscriberCallback(const std_msgs::UInt16 & ess_msg) {
if (ess_msg.data == 1)
{
    // digitalWrite(ESS, HIGH);
    PWR = true;
} else {
    // digitalWrite(ESS, LOW);
    PWR = false;
}
}

// ros::Publisher
// button_publisher("button_press", & button_msg);
ros::Subscriber < std_msgs::UInt16 > led_subscriber("toggle_led", & subscriberCallback);

void setup ()
{
  // Serial.begin(9600);
  // while (!Serial) {
  //   ; // wait for serial port to connect. Needed for native USB port only
  // }
  pinMode(2, INPUT); //left motor
  pinMode(3, INPUT); // right motor
  pinMode(7, INPUT); // Toggle for Auto/Manual, most right switch
  pinMode(5, INPUT); // Toggle for Emergency Stop, most left switch
  pinMode(6, OUTPUT); // Output Pin for Left Motor
  pinMode(9, OUTPUT); // Output Pin for Right Motor
  analogWrite(6, 128); // Left Motor OutPut - 2.5v (not moving) 
  analogWrite(9, 128); // Right Motor Output - 2.5v (not moving)
  digitalWrite(13, HIGH);
  pinMode(in1, OUTPUT); //L298
  pinMode(in2, OUTPUT); //L298
  pinMode(10, OUTPUT); //ESS Red LED
  pinMode(11, OUTPUT); //ESS Green LED
  pinMode(ESS, OUTPUT); //Emergency Stop Relay
  node_handle.initNode(); //Init Subscriber Node
  node_handle.subscribe(led_subscriber);
  digitalWrite(ESS, HIGH); //Power On All Motors
// pinMode(BUTTON, INPUT); //Emergency Stop Button
// node_handle.advertise(button_publisher); //Emergency Stop button
}
void loop()
{
  //ESS
  node_handle.spinOnce();
  delay(1);
  //Manual Control
  Ch1 = pulseIn(2, HIGH);
  Ch2 = pulseIn(3, HIGH);
  Ch6 = pulseIn(7, HIGH); //To read the Auto Manual Pulse from channel 6
  Ch5 = pulseIn(5, LOW); // To read the Emergency pulse from channel 5
  // Serial.println(Ch6);
  // Serial.println(Ch5);
  // Serial.println("[AR] Arduino online!");
  // if(Serial.available() > 0) {
  //   estop = Serial.read();
  // }
  delay(500); //NEED TO PUT THIS IN ELSE WHOLE SYSTEM NOT WORK
  if (PWR == false || ((Ch5 > 16000) && (Ch5 < 18000))) {
    // Serial.println("[AR] EStop Activated!");
    digitalWrite(ESS, LOW);//Turns Off Motors
    digitalWrite(10, HIGH); //Red LED On
    digitalWrite(11, LOW);
    //colored(strip.Color(255,0,0)); // display red light
    //strip.show();
    }
    else{
      digitalWrite(ESS,HIGH); //Turns On Motors
      digitalWrite(10, LOW); //Red LED Off
      digitalWrite(11, HIGH); //Green LED On
      if ((Ch1>1530) && (Ch2>1530)) //forward
      {
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
      } else if ((Ch1 < 1460) && (Ch2 < 1460)) //reverse
      {
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
      }
      else {
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
      }
      // delay(2000);
    }
}
  // else {
  //   digitalWrite(ESS,HIGH); //Turns On Motors
  //   if (Ch6 > 1000) // auto mode on (switch down)
  //     {
  //       //colored(strip.Color(0,255,0)); //green light
  //       // send signal to run program
  //     }
  //     else { 
  //     // add yellow light , manual control 
  //       if ((Ch1 == 0) && (Ch2 == 0))
  //       {
  //         analogWrite(6, 128); // Turns Left Motor Speed to 0
  //         analogWrite(9, 128); // Turns Right Motor Speed to 0
  //         delay(2000);
  //       }

  //       else if ((Ch1 > 1530) && (Ch2 > 1530)) // forward
  //       {
  //         MotorL = map (Ch1, 1530, 2000, 129, 255);
  //         MotorR = map (Ch2, 1530, 2000, 129, 255);
  //         analogWrite(6, MotorL); // Turns Left Motor Speed to forward
  //         analogWrite(9, MotorR); // Turns Right Motor Speed to forward 
  //         delay(2000);
  //       }

  //       else if ((Ch1 > 1530) && (Ch2 < 1460)) // turn right
  //       {
  //         MotorL = map (Ch1, 1530, 2000, 129, 255);
  //         MotorR = map (Ch2, 900, 1500, 0, 127);
  //         analogWrite(6, MotorL); // Turns Left Motor Speed to forward
  //         analogWrite(9, MotorR); // Turns Right Motor Speed to reverse 
  //         delay(2000);
  //       }

  //       else if ((Ch1 < 1460) && (Ch2 > 1530)) // turn left
  //       {
  //         MotorL = map (Ch1, 600, 1500, 0, 127);
  //         MotorR = map (Ch2, 1530, 2000, 129, 255);
  //         analogWrite(6, MotorL); // Turns Left Motor Speed to reverse
  //         analogWrite(9, MotorR); // Turns Right Motor Speed to forward 
  //         delay(2000);
  //       }

  //       else if ((Ch1 < 1460) && (Ch2 < 1460)) //reverse
  //       { 
  //         MotorL = map (Ch1, 900, 1500, 0, 127);
  //         MotorR = map (Ch2, 900, 1500, 0, 127); 
  //         analogWrite(6, MotorL); // Turns Left Motor Speed to reverse
  //         analogWrite(9, MotorR); // Turns Right Motor Speed to reverse 
  //         delay(2000);
  //       }
  //       else
  //       {
  //         analogWrite(6, 128); // Turns Left Motor Speed to 0
  //         analogWrite(9, 128); // Turns Right Motor Speed to 0
  //         // delay(2000);
  //       }
  //     }