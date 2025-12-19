#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.conditions import IfCondition

from ros_gz_bridge.actions import RosGzBridge

def generate_launch_description():

    # packages
    pkg_dir = get_package_share_directory('mpl_pose_tracking')
    sim_robot = get_package_share_directory('otto_gazebo')
    vex_fields = get_package_share_directory('pushback_sim')

    # file paths
    bridge_file = os.path.join(pkg_dir, 'config', 'gz_bridge.yaml')

    # launch arguments
    teleop_cmd = DeclareLaunchArgument(
        'teleop_toggle',
        default_value = 'true',
        description = 'select the drive method for the sim robot, '
    )

    declare_bridge_name_cmd = DeclareLaunchArgument(
        'bridge_name', 
        default_value="gt_bridge", 
        description='Name of ros_gz_bridge node'
    )

    declare_config_file_cmd = DeclareLaunchArgument(
        'config_file', 
        default_value = bridge_file, 
        description='YAML config file'
    )

    # Convert to launch config variable
    teleop_toggle = LaunchConfiguration('teleop_toggle')

    # gazebo bridge for ground truth of robot model
    gazebo_bridge = RosGzBridge(
        bridge_name=LaunchConfiguration('bridge_name'),
        config_file=LaunchConfiguration('config_file'),
    )

    # world launch file
    gazebo_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(vex_fields, 'launch', 'world_select.launch.py')),
        launch_arguments={'world': 'pushback_no_blocks'}.items()
    )

    # spawn robot
    otto = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(sim_robot, 'launch', 'spawn_robot.launch.py')),
        launch_arguments={'x_pose': '0.5','y_pose':'0.5'}.items()
    )

    # localization launch file
    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(sim_robot, 'launch', 'localization.launch.py'))
    )

    # enable teleop control
    drive_option_teleop = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(sim_robot, 'launch', 'controller.launch.py')),
        condition = IfCondition(teleop_toggle)
    )
    
    return LaunchDescription([
        teleop_cmd,
        declare_bridge_name_cmd,
        declare_config_file_cmd,
        gazebo_world,
        gazebo_bridge,
        otto,
        localization,
        drive_option_teleop
        ])
