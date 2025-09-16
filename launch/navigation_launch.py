import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration 

def generate_launch_description():
    package_name = 'round_bot'
    pkg_share = get_package_share_directory(package_name)
    
    localization_params_file = os.path.join(pkg_share, 'config', 'localization.yaml')
    # nav2_params_file = os.path.join(pkg_share, 'config', 'nav2_params_3d.yaml')
    nav2_params_file = os.path.join(pkg_share, 'config', 'nav2_params.yaml')
    rviz_file = os.path.join(pkg_share, 'rviz', 'navigation.rviz')
    map_yaml_file = os.path.join(pkg_share, 'maps', 'edifice.yaml')  # the map file path can be given in the yaml file, if the map file path mentioned there, no need to give in the nav2_map_server node
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    
    remappings = [('/tf', 'tf'), ('/tf_static', 'tf_static')]
    
    lifecycle_nodes_localization = ['map_server', 'amcl']
    lifecycle_nodes_nav2 = [
        'controller_server', 'smoother_server', 'planner_server',
        'behavior_server', 'velocity_smoother', 'bt_navigator', 'waypoint_follower'
    ]
    
    # Declare launch arguments
    declare_use_sim_time_cmd = DeclareLaunchArgument('use_sim_time', default_value='false', description='Use simulation time')
    declare_autostart_cmd = DeclareLaunchArgument('autostart', default_value='true', description='Auto start nav2 stack')

    bring_up = IncludeLaunchDescription(
              PythonLaunchDescriptionSource([os.path.join(
                  get_package_share_directory(package_name),'launch','bringup_launch.py'
              )]),
              launch_arguments={'rviz_launch': 'false'}.items() 
  )

    # Lifecycle Manager for localization
    localize_lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{'autostart': autostart}, {'node_names': lifecycle_nodes_localization}],
    )
    
    # Start Localization Nodes
    nav2_map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[localization_params_file, {'yaml_filename': map_yaml_file}],
        remappings=remappings,
    )
    
    nav2_amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[localization_params_file],
        remappings=remappings,
    )

    # Start RViz
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_file],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
    )
    
    # Start Nav2 Nodes
    nav2_controller = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav2_params_file],
    )
    
    nav2_smoother = Node(
        package='nav2_smoother',
        executable='smoother_server',
        name='smoother_server',
        output='screen',
        parameters=[nav2_params_file],
        remappings=remappings,
    )
    
    nav2_planner = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_params_file],
        remappings=remappings,
    )
    
    nav2_behaviors = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[nav2_params_file],
        remappings=remappings,
    )
    
    nav2_bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_params_file],
        remappings=remappings,
    )
    
    nav2_waypoint_follower = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=[nav2_params_file],
        remappings=remappings,
    )
    
    nav2_velocity_smoother = Node(
        package='nav2_velocity_smoother',
        executable='velocity_smoother',
        name='velocity_smoother',
        output='screen',
        parameters=[nav2_params_file],
        remappings=remappings,
    )
    
    # Lifecycle Manager for Nav2
    nav2_lifecycle_nodes_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{'autostart': autostart}, {'node_names': lifecycle_nodes_nav2}],
    )

    # Create the launch description and populate it with the actions
    ld = LaunchDescription()

    # Declare launch arguments
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_autostart_cmd)

    # Add nodes to launch
    # ld.add_action(bring_up)
    ld.add_action(rviz_node)
    ld.add_action(nav2_map_server)
    ld.add_action(nav2_amcl)
    ld.add_action(localize_lifecycle_manager)
    ld.add_action(nav2_controller)
    ld.add_action(nav2_smoother)
    ld.add_action(nav2_planner)
    ld.add_action(nav2_behaviors)
    ld.add_action(nav2_bt_navigator)
    ld.add_action(nav2_waypoint_follower)
    ld.add_action(nav2_velocity_smoother)
    ld.add_action(nav2_lifecycle_nodes_manager)

    return ld
