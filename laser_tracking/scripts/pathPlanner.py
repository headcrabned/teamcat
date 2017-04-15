#!/usr/bin/env python
import rospy
import tf.transformations
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped #laser location
from geometry_msgs.msg import Twist #high level motor control (linear and angular bot velocity)
from nav_msgs.msg import Odometry #Get the robot position


#Called whenever a laser position is published.
def goalCB(data):
    position = msg.pose.position
    #This code is called whenever a message is recieved.
    #There are a lot of components in a PoseStamped, but we just need x,y,z:
    rospy.loginfo("Point Position: [ %f, %f, %f ]"%(position.x, position.y, position.z))

    #Based on x,y,z, and the robot's x,y,z, choose a twist linear and angular velocity here

    #publish the twist command
    #For example, here's a program that just drives in a circle forever, regardless of laser
    # Twist is a datatype for velocity
    move_cmd = Twist()
    # let's go forward at 0.2 m/s
    move_cmd.linear.x = 0.2
    # let's turn at 0 radians/s
    move_cmd.angular.z = 0.5
    try:
        self.cmd_vel.publish(move_cmd)
    except CvBridgeError as e:
        print(e)

#Callback for getting robot position data
def odometryCb(msg):
    robotPos = msg.pose.pose.position
    robX = robotPos.x
    robY = robotPos.y
    robZ = robotPos.z
    robAngle = msg.twist.twist.angular.z #Not sure if this is the correct axis
    #Get the position error by subtracting these from the goal 

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.


    #Listener
    rospy.init_node('laserListener', anonymous=True)
    rospy.Subscriber('/move_base_simple/goal', PoseStamped, goalCB)
    rospy.Subscriber('odom',Odometry,odometryCb)
    
    #Publishers:
    pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
    #rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    #rospy.init_node('oodometry', anonymous=True) #make node 
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
