#!/usr/bin/env python
import rospy
import tf
import std_msgs.msg
from geometry_msgs.msg import PoseStamped #laser location
from geometry_msgs.msg import Twist #high level motor control (linear and angular bot velocity)
from nav_msgs.msg import Odometry #Get the robot position
from WheelVelocitys import CalculateWheelVelocity


#Called whenever a laser position is published.
def goalCB(data):
    global goal
    goal = data
    #goal = data.pose.position
    #This code is called whenever a message is recieved.
    #There are a lot of components in a PoseStamped, but we just need x,y,z:
    #rospy.loginfo("Point Position: [ %f, %f, %f ]"%(goal.x, goal.y, goal.z))
    print "Bot relative goal: x:%f, y:%f"%(goal.pose.position.x, goal.pose.position.y)

#Callback for getting robot position data, also plan and publish commands @100Hz
def odometryCb(data):
    pass
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
        CalculateWheelVelocity(-goal.y,goal.x) #Positive X is forward in the robot's frame, -y is right
        move_cmd.linear.x = .2
        move_cmd.angular.z = phi
    except:
        #If these haven't been initialized yet, spin
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = 0.5
    finally:
        pub.publish(move_cmd)


if __name__ == '__main__':

    #Listener
    rospy.init_node('laserListener', anonymous=True)
    rospy.Subscriber('/move_base_simple/goal', PoseStamped, goalCB)
    rospy.Subscriber('odom',Odometry,odometryCb)
    tflistener = tf.TransformListener()
    
    #Publishers:
    global pub
    pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=10)
    #rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1.0) # 10hz

    while not rospy.is_shutdown():
        
        try:
            #print "trying"
            t_now = rospy.get_rostime() #Update the goal so it's relative to the current robot position
            goal.header.stamp = t_now
            tflistener.waitForTransform('base_link','odom',t_now,rospy.Duration(4.0)) #Make sure we have tf data before doing this
            localGoal = tflistener.transformPose('odom',goal) #transform nav goal to relative coordinate frame
            
        except Exception as e:
            #print str(e)
            continue
            #rospy.sleep(1) #Wait a second for a first goal to come in.
            #continue
        x = localGoal.pose.position.x
        y = localGoal.pose.position.y
        CalculateWheelVelocity(-y,x) #Positive X is forward in the robot's frame, -y is right