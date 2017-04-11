/*
 * WheelVelocity.cpp
 *
 *  Created on: Apr 10, 2017
 *      Author: Nicholas
 */

#include <iostream>
#include <math.h>

struct WheelVelocity
{
    double left;
    double right;
};
WheelVelocity CalculateWheelVelocities(double targetX, double targetY, double orientation);
int main() {
    WheelVelocity Test = CalculateWheelVelocities(214,400, 0);
    std::cout << "Right Wheel Velocity " + std::to_string(Test.right) << std::endl;
    std::cout << "Left Wheel Velocity " + std::to_string(Test.left) << std::endl;
    return 0;
}
WheelVelocity CalculateWheelVelocities(double targetX, double targetY, double orientation)
{
    double RobotHomeX = 0;
    double RobotHomeY = 0;
    double wheelOffset = 1; // distance from wheel to wheel drive center
    double wheelLHomeX, wheelRHomeX, wheelLHomeY, wheelRHomeY;
    double wheelRTargetX, wheelLTargetX, wheelRTargetY, wheelLTargetY;
    double wheel_opp, wheel_adj;
    double driveDistance = sqrt((targetX * targetX) + (targetY * targetY));
    double thetaCarInv = targetX / driveDistance;
    double thetaCar = acos(thetaCarInv);//Angle of the point in reference to the origin
    double thetaRef = 0;
    double wheelLVelocity, wheelRVelocity;

    if (targetX > 0)
    {
        thetaCar = thetaCar - 90;
        thetaRef = 90 - abs(thetaCar);
    }

    if (targetX < 0)
    {
        thetaCar = thetaCar - 90;
        thetaRef = 90 - thetaCar;
    }

    if (targetX == 0) {
        thetaCar = 0;
    }

    // Set wheel home positions:
    wheelLHomeX = RobotHomeX - wheelOffset;
    wheelRHomeX = RobotHomeX + wheelOffset;
    wheelLHomeY = RobotHomeY;
    wheelRHomeY = RobotHomeY;

    // Calculate Targe wheel positions:
    //SOH
    wheel_opp = sin(thetaRef) * wheelOffset;
    wheelLTargetX = targetX - wheel_opp;
    wheelRTargetX = targetX + wheel_opp;
    wheel_adj = sqrt(wheelOffset - (wheel_opp * wheel_opp));

    if (thetaCar < 0)
    {
        wheelLTargetY = targetY + wheel_adj;
        wheelRTargetY = targetY - wheel_adj;
    }

    if (thetaCar > 0)
    {
        wheelLTargetY = targetY - wheel_adj;
        wheelRTargetY = targetY + wheel_adj;
    }

    double changeInXL = wheelLTargetX - wheelLHomeX;
    double changeInYL = wheelLTargetY - wheelLHomeY;
    double changeInXR = wheelRTargetX - wheelRHomeX;
    double changeInYR = wheelRTargetY - wheelRHomeY;
    double wheelLTravel = sqrt((changeInXL * changeInXL) + (changeInYL * changeInYL));
    double wheelRTravel = sqrt((changeInXR * changeInXR) + (changeInYR * changeInYR));

    // Set wheel velocity ratio:
    if (wheelLTravel > wheelRTravel)
    {
        wheelRVelocity = 1;
        wheelLVelocity = wheelLTravel / wheelRTravel;
    }

    if (wheelLTravel < wheelRTravel)
    {
        wheelLVelocity = 1;
        wheelRVelocity = wheelRTravel / wheelLTravel;
    }

    if (wheelLTravel == wheelRTravel)
    {
        wheelLVelocity = 1;
        wheelRVelocity = 1;
    }
    WheelVelocity wheelVel;
    wheelVel.left = wheelLVelocity;
    wheelVel.right = wheelRVelocity;

    return wheelVel;
}

