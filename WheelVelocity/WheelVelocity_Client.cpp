#include "ros/ros.h"
#include <cstdlib>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "WheelVelocity_client");
  if (argc != 3)
  {
    ROS_INFO("usage: WheelVelocity_client X Y");
    return 1;
  }

  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<beginner_tutorials::WheelVelocity>("WheelVelocity");
  beginner_tutorials::WheelVelocity srv;
  srv.request.a = atoll(argv[1]);
  srv.request.b = atoll(argv[2]);
  if (client.call(srv))
  {
    ROS_INFO("Left Wheel: %ld Right Wheel: %ld", (double)srv.response.LVelocity, (double)srv.response.RVelocity,);
  }
  else
  {
    ROS_ERROR("Failed to call service CalculateWheelVelocity");
    return 1;
  }

  return 0;
}
