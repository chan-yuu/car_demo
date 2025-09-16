# Ackermann Autonomous Car Simulation

## → Requirements

Before building and running the package, install the necessary dependencies using the `$ROS_DISTRO` environment variable:

```python
sudo apt-get install libeigen3-dev
sudo apt install ros-$ROS_DISTRO-joint-state-publisher-gui
sudo apt install ros-$ROS_DISTRO-xacro
sudo apt install ros-$ROS_DISTRO-gazebo-ros-pkgs
sudo apt install ros-$ROS_DISTRO-ros2-control ros-$ROS_DISTRO-ros2-controllers
sudo apt install ros-$ROS_DISTRO-controller-manager
```

### → Step 1: Create a ROS2 Workspace

1. Open a terminal and **Set up ROS2**.
    
    ```bash
    source /opt/ros/foxy/setup.bash #for ros2 foxy
    source /opt/ros/humble/setup.bash #for ro2 humble
    ```
    
2. Create a directory for the workspace and navigate into it:
    
    ```bash
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws
    ```
    

### → Step 2: Clone the GitHub Repository

1. Navigate to the `src` directory:
    
    ```bash
    cd ~/ros2_ws/src
    ```
    
2. Clone the repository:
    
    ```
    git clone https://github.com/armando-genis/Ackermann-Autonomous-Car-Simulation.git
    ```
    

### → Step 3: Build the Package

1. Go back to the root of the workspace:
    
    ```bash
    cd ~/ros2_ws
    ```
    
2. Build the package:
    
    ```bash
    colcon build --packages-select niagara_model
    colcon build --packages-select velodyne_gazebo_plugins
    colcon build --packages-select waypoints_niagara_creator
    colcon build --packages-select waypoints_niagara_loader
    colcon build --packages-select waypoints_calculations
    ```
    
3. Source the workspace:
    
    ```bash
    source install/setup.bash
    ```
    

### → Step 4: Run the Simulation

1. To launch with Gazebo and Rviz:
    
    ```bash
    ros2 launch niagara_model display.launch.py
    ```
    
2. To launch with only Rviz:
    
    ```bash
    ros2 launch niagara_model display_gui.launch.py
    ```
    

### → Step 6: Moving the Car with `cmd_vel`

1. You can manually move the car using the `cmd_vel` command in the terminal. This command publishes velocity messages to control the car's movement:
    
    ```bash
    ros2 topic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}'
    ```
    
    - Replace the values in `{linear: {x: ...}}` and `{angular: {z: ...}}` to adjust the car's speed and direction:
        - `linear.x`: Controls forward and backward motion (positive values move forward, negative values move backward).
        - `angular.z`: Controls the turning rate (positive values turn left, negative values turn right).

### → Step 7: Run the Waypoints Creator

1. Launch the waypoints creation node:
    
    ```bash
    ros2 launch waypoints_niagara_creator waypoints.launch.py
    ```
    
    ### → Explanation of the Waypoints Creator
    
    - This tool uses the car's odometry data to generate waypoints along the car's path. It continuously tracks the vehicle's position and stores coordinates as waypoints, which can later be used for navigation and simulation purposes.
    - **Adjusting Waypoints Iteration:** You can control the iteration (spacing) of the waypoints by modifying the `interval_interval_` variable in the source code. Changing this variable allows you to create more or fewer waypoints, depending on how detailed you want the path to be.
    - By default, the waypoints are saved in a CSV file. In the source code (line 52), the file path is defined as:
        
        ```cpp
        std::string file_path_ = "/home/genis/Music/wp.csv";
        ```
        

### Step 8: Run the Waypoints Loader

1. Launch the waypoints loader node:
    
    ```bash
    ros2 launch waypoints_niagara_loader waypointsLoader.launch.py
    ```
    
    ### → Explanation of the Waypoints Loader
    
    - The Waypoints Loader reads the path from a CSV file (previously created by the Waypoints Creator) and publishes it. This path can then be used for various purposes, such as processing the trajectory data or visualizing the path in Rviz2.
    - In the source code (approximately line 49), the path to the CSV file is set as follows:
        
        ```cpp
        std::string file_path_ = "/home/genis/Music/wp.csv";
        ```
        
    - **Make sure to change this path** to the location where your CSV file is stored. Update it to match a valid directory on your system before running the loader. This step is crucial for successfully loading the waypoints.

### →Step 2: Run the Waypoints Calculations

1. Launch the waypoints calculations node:
    
    ```bash
    ros2 launch waypoints_calculations calculation.launch.py
    ```
    
    ### → Explanation of the Waypoints Calculations
    
    - This package uses the car's **odometry** data and the pre-defined **path** to calculate a "lookahead" point. The lookahead point is a target on the path that the car will try to reach as it moves forward. This approach ensures smoother and more accurate path-following.
    
    ### → Configuration File Parameters
    
    The Waypoints Calculations package uses a configuration YAML file with parameters that define how the calculations are performed:
    
    ```yaml
    yaml
    Copiar código
    waypoints_calculations:
      ros__parameters:
        lookahead_min: 2.0
        lookahead_max: 5.0
        mps_alpha: 1.0
        mps_beta: 3.5
    
    ```
    
    - **`lookahead_min`**: The minimum lookahead distance for the car while following the path.
    - **`lookahead_max`**: The maximum lookahead distance, which limits how far ahead the car will consider waypoints.
    - **`mps_alpha`** and **`mps_beta`**: Parameters used for speed and steering calculations, affecting how the car navigates through the waypoints.