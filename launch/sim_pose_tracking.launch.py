#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, FindExecutable
from launch.conditions import IfCondition

from ros_gz_bridge.actions import RosGzBridge

def generate_launch_description():

    # packages
    pkg_dir = get_package_share_directory('mpl_pose_tracking')
    sim_robot = get_package_share_directory('otto_gazebo')
    robot_bringup = get_package_share_directory('otto_bringup')
    vex_fields = get_package_share_directory('pushback_sim')

    # file paths
    bridge_file = os.path.join(pkg_dir, 'config', 'ground_truth_bridge.yaml')

    # teleop toggle argument
    teleop_toggle = LaunchConfiguration('teleop')
    teleop_cmd = DeclareLaunchArgument(
        'teleop',
        default_value='true',  
        description='select the drive method for the sim robot, '
    )

    # name of the robot pose bridge argument
    bridge_name = LaunchConfiguration('bridge_name')
    declare_bridge_name_cmd = DeclareLaunchArgument(
        'bridge_name', 
        default_value="robot_pose_bridge", 
        description='Name of ros_gz_bridge node for getting the ground truth pose of the robot'
    )

    # gazebo robot pose bridge config file
    bridge_config_file = LaunchConfiguration('bridge_config_file')
    declare_config_file_cmd = DeclareLaunchArgument(
        'bridge_config_file', 
        default_value=bridge_file,  
        description='YAML config file'
    )

    # rosbag recording argument
    rosbag_toggle = LaunchConfiguration('rosbag')
    rosbag_rec_cmd = DeclareLaunchArgument(
        'rosbag',
        default_value='false', 
        description='toggle recording rosbags'
    )

    # gazebo bridge for ground truth of robot model
    gazebo_poses = RosGzBridge(
        bridge_name=bridge_name,
        config_file=bridge_config_file,
    )

    # world launch file
    gazebo_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(vex_fields, 'launch', 'world_select.launch.py')),
        launch_arguments={'world': 'empty_field'}.items()
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


    # localization launch file
    map_only = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(sim_robot, 'launch', 'map_server.launch.py'))
    )

   
    # enable teleop control
    drive_option_teleop = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(robot_bringup, 'launch', 'controller.launch.py')),
        condition = IfCondition(teleop_toggle)
    )

    rosbag = ExecuteProcess(
        cmd=[[
            FindExecutable(name='ros2'),
            'bag',
            'record',
             '/robot_pose',
             '/amcl_pose',
            '-o', f'~/rosbags/']],
        shell=True
    )

    rosbag_delay = TimerAction(
        condition=IfCondition(rosbag_toggle),
        period=3.0,
        actions=[rosbag]                   
    )

    return LaunchDescription([
        rosbag_rec_cmd,
        teleop_cmd,
        declare_bridge_name_cmd,
        declare_config_file_cmd,
        gazebo_world,
        otto,
        localization,
        map_only,
        gazebo_poses, 
        drive_option_teleop,
       # rosbag_delay
        ])