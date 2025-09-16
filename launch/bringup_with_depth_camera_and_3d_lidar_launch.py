import os
from launch import LaunchDescription
from launch.substitutions import Command,  LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.conditions import IfCondition
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
  package_name = 'round_bot'
  pkg_share = get_package_share_directory(package_name)

  xacro_file_path = os.path.join(pkg_share, 'description', 'round_bot_with_depth_camera_and_3d_lidar.urdf.xacro')
  world_file = os.path.join(pkg_share, "worlds", "office_floor_plan.world")
  robot_description = Command(['xacro ', xacro_file_path])
  
  rviz_launch = LaunchConfiguration('rviz_launch', default='true') 
  
  rviz_node = Node(
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    arguments=['-d', os.path.join(pkg_share, 'rviz', 'visualize_with_depth_camera.rviz')],
    output='screen',
    parameters=[{'use_sim_time': True}],
    condition=IfCondition(rviz_launch),
  )

  robot_state_publisher = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    name='robot_state_publisher',
    output='both',
    parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
  )

  joint_state_publisher = Node(
    package='joint_state_publisher',
    executable='joint_state_publisher',
    name='joint_state_publisher',
    output='both',
    parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
  )
  
  gazebo = ExecuteProcess(
    cmd=['gazebo', '--verbose', world_file,  '-s', 'libgazebo_ros_factory.so'] #os.path.join(pkg_share, 'worlds', 'your_world_file.world')],
  )

  spawn_entity = Node(
    package= 'gazebo_ros',
    executable= 'spawn_entity.py',
    name = 'urdf_spawner',
    output = 'screen',
    arguments = ['-topic', '/robot_description', '-entity', 'round_bot', '-x', '0.0', '-y', '0.0', '-z', '0.0',
    '-R', '0.0', '-P', '0.0', '-Y', '1.57'],
    parameters=[{'use_sim_time': True}],
  )

  return LaunchDescription([
    rviz_node,
    robot_state_publisher,
    joint_state_publisher,
    gazebo,
    spawn_entity
  ])


