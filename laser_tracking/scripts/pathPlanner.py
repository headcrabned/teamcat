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
    print "Bot absolute goal: x:%f, y:%f"%(goal.pose.position.x, goal.pose.position.y)


if __name__ == '__main__':

    #Listener
    rospy.init_node('laserListener', anonymous=True)
    rospy.Subscriber('/move_base_simple/goal', PoseStamped, goalCB) #in odom frame
    tflistener = tf.TransformListener()
    
    #Publishers:
    pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=10)
    #rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        v = 0
        phi = 0
        try:
            #print "trying"
            t_now = rospy.get_rostime() #Update the goal so it's relative to the current robot position
            goal.header.stamp = t_now
            #tflistener.waitForTransform('base_link','odom',t_now,rospy.Duration(4.0)) #Make sure we have tf data before doing this
            #localGoal = tflistener.transformPose('odom',goal) #transform nav goal to relative coordinate frame
            tflistener.waitForTransform('odom','base_link',t_now,rospy.Duration(4.0)) #Make sure we have tf data before doing this
            localGoal = tflistener.transformPose('base_link',goal) #transform nav goal to relative coordinate frame
            
        except Exception as e:
            #print str(e)
            continue
            #rospy.sleep(1) #Wait a second for a first goal to come in.
            #continue
        x = localGoal.pose.position.x
        y = localGoal.pose.position.y
        print("localx:",x,"localy:",y)
        (v,phi) = CalculateWheelVelocity(-y,x) #Positive X is forward in the robot's frame, -y is right
        #rospy.spin()
        move_cmd = Twist()
        move_cmd.linear.x = v
        move_cmd.angular.z = phi
        pub.publish(move_cmd)