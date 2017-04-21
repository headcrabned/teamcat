#!/usr/bin/env python
import rospy
import tf.transformations
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped #laser location
from geometry_msgs.msg import Twist #high level motor control (linear and angular bot velocity)
from nav_msgs.msg import Odometry #Get the robot position


#Called whenever a laser position is published.
def goalCB(data):
    goal = data.pose.position
    #This code is called whenever a message is recieved.
    #There are a lot of components in a PoseStamped, but we just need x,y,z:
    rospy.loginfo("Point Position: [ %f, %f, %f ]"%(goal.x, goal.y, goal.z))

#Callback for getting robot position data, also plan and publish commands @100Hz
def odometryCb(data):
    robotPos = data.pose.pose.position
    robX = robotPos.x
    robY = robotPos.y
    robZ = robotPos.z
    robAngle = data.twist.twist.angular.z #Not sure if this is the correct axis

    #########Call the path planner function here, get the resultant velocity and angular velocity
    #(v,phi)=plan(robX,robY)

    #publish the twist command
    #For example, here's a program that just drives in a circle forever, regardless of laser
    # Twist is a datatype for velocity
    move_cmd = Twist()
    # let's go forward at 0.2 m/s
    try:
        move_cmd.linear.x = v
        move_cmd.angular.z = phi
    except:
        #If these haven't been initialized yet, spin
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = 0.5
    finally:
        pub.publish(move_cmd)

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
    global pub
    pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=10)
    #rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    #rospy.init_node('oodometry', anonymous=True) #make node 
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
