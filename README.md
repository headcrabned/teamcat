# teamcat
ROS project to follow a laser pointer with Turtlebot
Clone this repository into carkin_ws/src

Build the package by running:
cd catkin_ws
catkin_make

Try Gazebo examples by running:
roslaunch laser_tracking env_bringup.launch
or
roslaunch laser_tracking amcl_demo_full.launch

To understand data / control flow, try
rqt_graph
or 
rostopic list
