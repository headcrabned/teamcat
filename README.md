# teamcat
ROS project to follow a laser pointer with Turtlebot, using PID control

To run this simulation:
Install Ubuntu 14 LTS (but it will likely work on other versions)

Run "ROSSetup.sh" to install ROS and the other project dependencies

Clone this repository into carkin_ws/src

Build the package by running:

cd catkin_ws

catkin_make

Try Gazebo examples by running:

roslaunch laser_tracking env_bringup.launch
or

roslaunch laser_tracking amcl_demo_full.launch

Finally to run the controller, close the other ROS demos
Open 2 terminals, and in one run:

roslaunch laser_tracking env_test.launch
In the second terminal,:

roslaunch laser_tracking pidPlanner.py

When RViz opens, load the "blind navigation" configuration
Publish 2D navigation goals in RViz.

To understand data / control flow, try using
rqt_graph

or 
rostopic list
