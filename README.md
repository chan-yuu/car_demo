# Round Bot
This package contains creating 2d costmap and 3d costmap using STVL(Spatio Temporal Vortex Layer) for the navigation implemented on the round_bot in the simulation.

## Requirements
* Ubuntu - 22.04
* ROS2 - Humble

### Workflow for the 2d costmap and navigation

![gif_example](https://github.com/Vasanth28897/round_bot/blob/humble_gazebo_classic/docs/gifs/2d_costmap_navigation.gif)

* To drive and play with the round_bot, launch this command

    ```bash
    ros2 launch round_bot bringup_launch.py
    
    ```

* Drive the round_bot using this command in the terminal

    ```bash
    ros2 run teleop_twist_keyboard teleop_twist_keyboard
    
    ```

* To generate a slam, use this command(use the teleop_twist_keyboard to drive and map the environment)

    ```bash
    ros2 launch round_bot slam_launch.py
    
    ```

* Use this command to save the map file after map is generated

    ```bash
    ros2 run nav2_map_server map_saver_cli -f map_folder/map_file_name
    
    ```


* To make the round_bot go autonomously, use this below command (Note : Don't forget to add the map_filename.yaml file in the navigation_launch.py file)

    ```bash
    ros2 launch round_bot navigation_launch.py
    
    ```

    the round bot localize automatically, you can send the goal using  `2d_goal` in the rviz, or you can send the `send_goal` command like this below in another terminal

    ```bash
    ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "{pose: {header: {stamp: {sec: 0, nanosec: 0}, frame_id: 'map'}, pose: {position: {x: 3.0, y: 3.0, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}"
    
    ```


### Workflow for the 3d costmap and navigation 

Available Plug&Play Setups 
--------------------------
### STVL Observation Sources
I used two different sensors to build the voxel grid in this package: 3D LiDAR and a depth camera(mounted in the front of the round bot).

* To drive and play with the round_bot, launch this command

    ```bash
    ros2 launch round_bot bringup_with_depth_camera_and_3d_lidar_launch.
    
    ```

* Drive the round_bot using this command in the terminal

    ```bash
    ros2 run teleop_twist_keyboard teleop_twist_keyboard
    
    ```

* To generate a slam, use this command(use the teleop_twist_keyboard to drive and map the environment)

    ```bash
    ros2 launch round_bot slam_with_depth_camera_and_3d_lidar_launch.py
    
    ```

* Use this command to save the map file after map is generated

    ```bash
    ros2 run nav2_map_server map_saver_cli -f map_folder/map_file_name
    
    ```


* To make the round_bot go autonomously, use this below command (Note : Don't forget to add the map_filename.yaml file in the navigation_launch.py file).
* If you want to use the 3d_lidar for the voxel grid, change the `SENSOR` name as `3d_lidar` or if you want to use the depth_camera for the voxel grid change the `SENSOR` name as `camera` in the `navigation_with_stvl_launch.py` file.

stvl with 3d_lidar

![gif_example](https://github.com/Vasanth28897/round_bot/blob/humble_gazebo_classic/docs/gifs/3d_costmap_navigation_with_3d_lidar.gif)

stvl with camera

![gif_example](https://github.com/Vasanth28897/round_bot/blob/humble_gazebo_classic/docs/gifs/3d_costmap_navigation_with_camera.gif)

 
    ```bash
    ros2 launch round_bot navigation_with_stvl_launch.py
    ```

the round bot localize automatically, you can send the goal using  `2d_goal` in the rviz, or you can send the `send_goal` command like this below in another terminal

    ```bash
    ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "{pose: {header: {stamp: {sec: 0, nanosec: 0}, frame_id: 'map'}, pose: {position: {x: 3.0, y: 3.0, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}"
    
    ```


## References
* [Spatio-Temporal Voxel Layer](https://github.com/SteveMacenski/spatio_temporal_voxel_layer) GitHub repository

* [ros2-navigations-stvl](https://github.com/mich-pest/ros2_navigation_stvl) Github repository.
