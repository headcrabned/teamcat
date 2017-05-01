#!/usr/bin/env python
import rospy
import tf
import std_msgs.msg
from math import atan2, hypot
from geometry_msgs.msg import PoseStamped #laser location
from geometry_msgs.msg import Twist #high level motor control (linear and angular bot velocity)
from nav_msgs.msg import Odometry #Get the robot position
from WheelVelocitys import CalculateWheelVelocity
from pid_control import PID


#Called whenever a laser position is published.
def goalCB(data):
    global goal
    goal = data
    #goal = data.pose.position
    #This code is called whenever a message is recieved.
    #There are a lot of components in a PoseStamped, but we just need x,y,z:
    #rospy.loginfo("Point Position: [ %f, %f, %f ]"%(goal.x, goal.y, goal.z))
    print "Bot absolute goal: x:%f, y:%f"%(goal.pose.position.x, goal.pose.position.y)


if __name__ == '__main__':

    #Listener
    rospy.init_node('laserListener', anonymous=True)
    rospy.Subscriber('/move_base_simple/goal', PoseStamped, goalCB) #in odom frame
    tflistener = tf.TransformListener()
    
    #Publishers:
    pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=10)
    rate = rospy.Rate(60) # 60hz

    #  PID Terms:    P   I   D I_max
    angle_pid = PID(7.0,0.0,3.0,0.2) #Tuned Parameters
    #angle_pid = PID(7.0,0.0,0.0,0.2) #Undamped Parameters
    #angle_pid = PID(7.0,0.0,1.0,0.2) #Underdamped Parameters
    #angle_pid = PID(1.0,0.0,25.0,0.2) #Overdamped Parameters
    t_last = 0.
    while not rospy.is_shutdown():
        v = 0.
        phi = 0.
        try:
            t_now = rospy.get_rostime() #Update the goal so it's relative to the current robot position
            goal.header.stamp = t_now
            tflistener.waitForTransform('odom','base_link',t_now,rospy.Duration(4.0)) #Make sure we have tf data before doing this
            localGoal = tflistener.transformPose('base_link',goal) #transform nav goal to relative coordinate frame
            
        except Exception as e:
            #print str(e)
            continue
            #rospy.sleep(1) #Wait a second for a first goal to come in.
            #continue

        #Do the actual control here!
        x = localGoal.pose.position.x
        y = localGoal.pose.position.y

        theta_err = atan2(-y,x) #different coordinate systems. Here x=1,y=0 is straight ahead.
        #phi = -1.0*theta_err
        phi = angle_pid.update(theta_err,t_now.to_sec())
        phi = max(min(phi,1.5),-1.5) #maximum hardware turning rate for turtlebot
        print angle_pid.debug()
        if hypot(x,y) > .05:
            v = .3
        else:
            v=0
            phi = 0
        #print("localx:",x,"localy:",y)
        #(v,phi) = CalculateWheelVelocity(-y,x) #Positive X is forward in the robot's frame, -y is right
        #rospy.spin()
        move_cmd = Twist()
        move_cmd.linear.x = v
        move_cmd.angular.z = phi
        pub.publish(move_cmd)
        rate.sleep()