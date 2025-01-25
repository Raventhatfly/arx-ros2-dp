# ROS2 Inference Script for ARX Arm

## Installation
Before started, please make sure that ros2 humble is installed.
First create a workspace:
```shell
mkdir dp_ws && cd dp_ws
mkdir src && cd src
```
Then clone the respotory:
```shell
git clone --recurisve git@github.com:Raventhatfly/arx-ros2-dp.git
```
Return to the workspace folder (in this example `dp_ws`) and build the package:
```shell
colcon build --symlink-install
```
Please make sure that conda is deactivated before build.

ROS2 utilize the python3.10 version, so make sure the following command is entered:
```shell
source /opt/ros/humble/setup.bash
```
And use pip to install the requirement. The requirement.txt can be found in the repo, but it is still under maintainence and not tested.

## History
01.25.2025 Updated the first version by Feiyang Wu.