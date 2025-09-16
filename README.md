# Round Bot
This package contains docker to execute the gazebo harmonic and the robot model(round_bot) and execute the slam and navigation in the local system.

## Requirements
* ROS2 - Humble
* Docker
* ROS2 - Navigation

## Objective
* I wanted to run the gazebo Harmonic and spawn the robot model in the gazebo inside the docker container alone.
* The slam and Navigation exection happening in the local system(host). 
* To establish the communication between docker container and the local sytem.
* If you want to check the repo in the github -> 
   [round_bot](https://github.com/Vasanth28897/round_bot)


## Cloning the repo
* Create a workspace to build the package
* under the src directory clone the repo from github

   ``` bash
   git clone -b humble-gazebo-latest https://github.com/Vasanth28897/round_bot.git
   ``` 

## Execution
* This below command build the docker container and image, the `Dockerfile` is placed under the docker directory

    ```bash
    docker build -t <image_name> .
    ```

* Make sure the docker image is created by using this command `docker images`. You must see this output like this

    ```bash
    pc@pc:~/round_bot_ws$ docker images
    REPOSITORY                    TAG                     IMAGE ID       CREATED        SIZE
    ros2-humble-gazebo-harmonic   latest                  84740332c855   8 hours ago    5.71GB
    ros                           humble-ros-core-jammy   97ffc2601d2f   3 months ago   424MB
    ```

* To run the docker container and access the docker volume 

    ``` bash
    ./src/round_bot/docker/run_image.sh
    ```
    After this command executed, the terminal looks like this
    ``` bash
    pc@pc:~/$ ./src/round_bot/docker/run_image.sh 
    Attaching to container round_bot_dev...
    root@pc:~/round_bot_ws# 
    ```

* Build the package 
    ```bash
    colcon build --symlink-install
    ```

* Make sure the RMW_IMPLEMENTATION set in both the local and the docker `.bashrc` file. Run this command in the terminal to see which DDS is installed 
`echo $RMW_IMPLEMENTATION` it has to give output `rmw_cyclonedds_cpp`. Otherwise set this using this command and source it. 
    
    ```bash
    echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
    ``` 
    ```bash
    source ~/.bashrc
    ``` 

* set the local host in the local system
    ```bash
    xhost +local:root
    ```

* If the build is succesfull, source the workspace and run the launch file to launch the gazebo and spawn the robot

    ```bash
    ros2 launch round_bot bringup_launch.py
    ```

![Simulation Image](https://github.com/Vasanth28897/round_bot/blob/humble_gazebo_latest/docs/robot_spawn.png)

* Check the listed topics in the local system 
    
    ```
    pc@pc:~/round_bot__ws$ ros2 topic list
    /camera/image_raw
    /clicked_point
    /clock
    /cmd_vel
    /goal_pose
    /initialpose
    /joint_states
    /odom
    /parameter_events
    /robot_description
    /rosout
    /scan
    /tf
    /tf_static
    ```
    
* Check the listed topics in the docker 
    
    ```bash
    root@pc:~/round_bot_harmonic_ws# gz topic -l
    /camera/camera_info
    /camera/image_raw
    /clock
    /cmd_vel
    /gazebo/resource_paths
    /gui/camera/pose
    /gui/record_video/stats
    /joint_states
    /keyboard/keypress
    /marker
    /model/Mecanum_lift/cmd_vel
    /model/Mecanum_lift/odometry
    /odom
    /scan
    /scan/points
    /sensors/marker
    /stats
    /subt_performer_detector
    /tf
    /world/Edifice/clock
    /world/Edifice/dynamic_pose/info
    /world/Edifice/pose/info
    /world/Edifice/scene/deletion
    /world/Edifice/scene/info
    /world/Edifice/state
    /world/Edifice/stats
    ```
* you can drive the robot using this command inside the container and from the host by the topic `/cmd_vel`

    ```bash
    ros2 run teleop_twist_keyboard teleop_twist_keyboard
    ```

## SLAM_TOOLBOX (run from the host)
* To generate a map, use this command(use the teleop_twist_keyboard to drive and map the environment). 

    ```bash
    ros2 launch round_bot slam_launch.py
    ```

* Use this command to save the map file after map is generated

    ```bash
    ros2 run nav2_map_server map_saver_cli -f workspace/src/round_bot/maps/map_file_name
    ```

## NAVIGATION (run from the host)
* To check the navigation, use this below command (Note : Don't forget to add the map_filename.yaml file in the navigation_launch.py file)

    ```bash
    ros2 launch round_bot navigation_launch.py
    ```

* Give the goal by pressing `2d_goal` and click anywhere in the map in rviz environment, or you can send the `send_goal` command like this below in another terminal

    ```bash
    ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "{pose: {header: {stamp: {sec: 0, nanosec: 0}, frame_id: 'map'}, pose: {position: {x: 3.0, y: 3.0, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}"
    ```
 
