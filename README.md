# Demo of Prius in ROS/GAZEBO
[![CI](https://github.com/NovoG93/car_demo/actions/workflows/CI.yml/badge.svg?event=push)](https://github.com/NovoG93/car_demo/actions/workflows/CI.yml)
[![CD](https://github.com/NovoG93/car_demo/actions/workflows/CD.yml/badge.svg?event=workflow_run)](https://github.com/NovoG93/car_demo/actions/workflows/CD.yml)

This is a simulation of a Prius in [gazebo 11](http://gazebosim.org) with sensor data being published using [ROS 2 foxy](http://wiki.ros.org/noetic/Installation)
The car's throttle, brake, steering, and gear shifting are controlled by publishing a ROS message.
A ROS node allows driving with a [gamepad/joystick](./car_demo/scripts/joystick_translator.py) (not yet tested) or [keyboard](./car_demo/scripts/prius_teleop_keyboard.py) (also directly in gazebo when [mcity.world](./car_demo/worlds/mcity.world) is loaded).

# Video + Pictures

A video and screenshots of the demo can be seen in this blog post: https://www.osrfoundation.org/simulated-car-demo/

<figure>
    <center>
        <table><tr>
            <td> <img src="./assets/rviz.png" title="Rviz overview" height="500"/> </td>
            <td> <img src="./assets/gazebo.jpg" title="Gazebo overview" height="500"/> </td>
        </tr></table>
        <figcaption>Sensor data of Prius in rviz2 (left), and gazebo simulation (right)</figcaption>
    </center>
</figure>

# Requirements

This demo has been tested on Ubuntu Xenial (20.04) with ROS2 Foxy and inside docker.

1. Using ROS2 Foxy installation:
   * [Install ROS2 Foxy](https://docs.ros.org/en/foxy/Installation.html)

2. Using Docker:
   * An X server
   * [Docker](https://www.docker.com/get-docker)
   * [nvidia-docker2](https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0))
   * The current user is a member of the docker group or other group with docker execution rights.
   * [rocker](https://github.com/osrf/rocker)

# Building

First clone the repo, then run the script `build_demo.bash`.
It builds a docker image with the local source code inside.


1. Using ROS2 Foxy installation:
```
$ cd ~/ros2_ws/
$ vcs import src < rosinstall.yaml
$ colcon build  --packages-up-to car_demo  --symlink-install 
```
2. Using Docker:
```
$ cd car_demo
$ ./build_demo.bash
```

# Running

1. Using ROS2 Foxy installation
```
$ source ~/ros2_ws/install/setup.bash
$ ros2 launch car_demo demo.launch.py
```
2. Using Docker
Use the script `run_demo.bash` to run the demo.
```
$ ./run_demo.bash
```
In both cases an [RVIZ](http://wiki.ros.org/rviz) window will open showing the car and sensor output.
A gazebo window will appear showing the simulation.
Either use the controller to drive the prius around the world, or click on the gazebo window and use the `WASD` keys to drive the car or use the teleop window that opens in xterm.