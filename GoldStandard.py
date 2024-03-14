'''
Vibha Kamath, Theresa Nguyen, Ege Cogulu

In this file we will get movement data based on what object and confidence 
level the robot is seeing, and move the robot based on that data. 
'''
import RPi.GPIO as GPIO
import time
import sys
import rclpy
from rclpy.node import Node
import random
import time
import DetermineObject

linear = 0
angular = 0

'''
Ultrasonic Sensor Setup
'''
# GPIO pins for the ultrasonic sensor
# See wiring diagram in /WiringDiagrams/Ultrasonic.png
GPIO_TRIGGER = 40
GPIO_ECHO = 38

GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

'''
For RotateAngle action
'''

from rclpy.action import ActionClient

# Import the RotateAngle action
from irobot_create_msgs.action import RotateAngle

'''
ROTATE ANGLE ACTION CLIENT CLASS
Subclass of Node Class
'''

runAgain = True 

class RotateAngleActionClient(Node):

    global runAgain

    # Define a method to initialize the node
    def __init__(self):

        # Initialize a node with the name rotate_angle_action_client
        super().__init__('rotate_angle_action_client')

        # Create an action client using the action type 'RotateAngle' that we imported above 
        # with the action name '/rotate_angle' which can be found by running `ros2 action list -t`
        self._action_client = ActionClient(self, RotateAngle, '/rotate_angle')

    # Define a method to send the goal to the action server
    def send_goal(self, angle, max_rotation_speed):

        # Create a variable for the goal request message to be sent to the action server
        goal_msg = RotateAngle.Goal()
        goal_msg.angle = angle
        goal_msg.max_rotation_speed = max_rotation_speed

        # Instruct the action client to wait for the action server to become available
        print("Waiting for server")
        self._action_client.wait_for_server()

        print("Sending goal request")
        # Send goal request to the server asynchronously, and set the feedback callback
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        print("Sent goal request")

        # Set a callback that executes a new function 'goal_response_callback'
        # when the future is complete, indicating whether the goal was accepted or rejected

        print("Sending Response Callback")
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        print("Sent Response Callback")

    # Define a response callback for when the future is complete
    def goal_response_callback(self, future):

        # Store the result of the future as 'goal_handle'
        goal_handle = future.result()

        # Check if the goal was accepted or rejected and print to the logger
        if not goal_handle.accepted:
            self.get_logger().info('Rotation rejected :(')
            return

        self.get_logger().info('Rotation accepted :)')

        # Request the result from the server
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    # Define a result callback for when the future is complete
    def get_result_callback(self, future):

        # Store the result from the server
        result = future.result().result

        # Print the result to the logger
        self.get_logger().info('Rotated.')
        #.format(result.success)

        # Shut down rclpy
        #rclpy.shutdown() # spinning once should solve this issue

    # Define a method to receive constant feedback from the feedback topic
    def feedback_callback(self, feedback_msg):

        # Print the received feedback messages to the logger
        self.get_logger().info('Received rotation feedback: {0}')
        #.format(feedback_msg.feedback.current_angle)


'''
MOVE PUBLISHER
These statements import Twist messages to send to /cmd_vel
'''
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

linear = 0
angular = 0

class MovePublisher(Node):
    global linear
    global angular
     #This class let's us create nodes

    def __init__(self):
        #creating the node
        super().__init__('moving')

        # Creates a publisher based on the message type "Vector3" that has been imported from the std_msgs module above
        # Sets the publisher to publish on the 'my_publisher' topic
        # Sets a queue size of 10 - essentially a backlog of messages if the subscriber isn't receiving them fast enough
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Set delay in seconds
        timer_period = .3 

        # Creates a timer that triggers a callback function after the set timer_period
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Sets initial counter to zero
        self.i = 0

     def timer_callback(self):
        dist = measure_distance()
        print(dist)
        if distance > 12:
            msg = Twist()
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.publisher.publish(msg)
            self.get_logger().info(f'Publishing: "{msg.linear.x}"')
            Straight = True
            print(counter)
        else:
            msg.linear.x = float(0)
            msg.angular.z = float(0)
            self.publisher.publish(msg) 
            # Prints `msg.data` to console
            self.get_logger().info('Publishing: "%s"' % msg.linear.x) 
            self.rotation()


    def rotation(self):

        rclpy.init(args=args)
        rotate_client = RotateAngleActionClient()
        moving = MovePublisher()
 
        while True:

            try:
                info = DetermineObject.ObjectAndLevel()
                thing = info[0] 
                thing = thing.replace('\n', '')
                confidence = int(info[1])
                
                if (confidence > 97): # it's seeing an object
                    print("Object confirmed! Moving...")
                    if (thing == "Bear"):
                        ClassOne_Bear(rotate_client)
                    elif (thing == "Darth Vader"):
                        ClassTwo_Vader(rotate_client)
                    elif (thing == "Elephant"):
                        ClassThree_Elephant(rotate_client)
                    elif (thing == "Kiwi"):
                        ClassFour_Kiwi(rotate_client)
                    elif (thing == "Mario"):
                        ClassFive_Mario(rotate_client)
                    elif (thing == "Mug"): 
                        ClassSix_Mug(rotate_client)
                    elif (thing == "Rubik's Cube"):
                        print("It's the Cube!")
                        ClassSeven_Cube
                        print("Called Cube function!")

   
'''
MOVEMENT FUNCTIONS
Called in the get_data() function, these change either the linear and angular 
velocity values to move straight or return rotation angles and speed to go 
left or right. 
'''

def turnLeft(rotate_client):
    # set (angle, speed)
    Rotate(1.5708, 0.5, rotate_client)

def turnRight(rotate_client):
    # set (angle, speed)
    Rotate(-1.5708, 0.5, rotate_client)

'''
OBJECT FUNCTIONS
Just determines whether the robot goes left or right for a given object.
These will be changed the day of the demo based on the maze.
'''

def ClassOne_Bear(rotate_client):
    turnLeft(rotate_client)

def ClassTwo_Vader(rotate_client):
    turnRight(rotate_client)

def ClassThree_Elephant(rotate_client):
    turnRight(rotate_client)

def ClassFour_Kiwi(rotate_client):
    turnRight(rotate_client)

def ClassFive_Mario(rotate_client):
    turnRight(rotate_client)

def ClassSix_Mug(rotate_client):
    turnLeft(rotate_client)

def ClassSeven_Cube(rotate_client):
    turnLeft(rotate_client)

def ClassEight_Empty(rotate_client):
    turnLeft(rotate_client)


'''
MOVEMENT AND ROTATION FUNCTIONS
Functions to actually send goals to the Create 3.
'''

def Move(args=None):
    
    global linear
    global angular

    rclpy.init(args=args)

    try:
        moving = MovePublisher()
        rclpy.spin(moving)

    except KeyboardInterrupt:
        print('Keyboard Interrupt')

    finally:
        #move_publisher.reset()
        moving.destroy_node()
        rclpy.shutdown()


def Rotate(angle, max_rotation_speed, rotate_client, args=None):
    global runAgain
    print("In Rotate!")
    # Call the send_goal method to send the rotate_angle goal to the action server
    rotate_client.send_goal(angle, max_rotation_speed)

    # Spin the node to activate callbacks and subscriptions
    rclpy.spin(rotate_client)

'''
ULTRASONIC SENSOR
Reads distance values
'''

def measure_distance():
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # Save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Time difference between start and arrival
    time_elapsed = stop_time - start_time
    print(time_elapsed)

    # Speed of sound in air (343 meters per second) and 100 for conversion to centimeters
    distance_cm = round((time_elapsed * 34300) / 2, 2)

    print("Distance:", distance_cm)
    
    time.sleep(0.1)

    return distance_cm

'''
MAIN
Loops timercallback() to constantly "see".
'''

def main(args=None):

    rclpy.init(args=args)
    rotate_client = RotateAngleActionClient()
    moving = MovePublisher()
 
    while True:

        try:
            moving.timer_callback() # will go straight if distance > 12 

        except KeyboardInterrupt:
            print(Interrupt)

if __name__ == '__main__':
    main()
