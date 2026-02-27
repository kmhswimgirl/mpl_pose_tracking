#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python import get_package_share_directory

def generate_launch_description():
    pkg_dir= get_package_share_directory('mpl_pose_tracking')
    config_file = os.path.join(pkg_dir, 'config', 'cams.yaml')
    apriltag_file = os.path.join(pkg_dir, 'config', 'apriltags.yaml')

    camera_node =  Node( # launches
        package='usb_cam', 
        executable='usb_cam_node_exe', 
        output='screen',
        name='field_cam',
        parameters=[config_file] # camera calibration is still messed up, need bigger checkerboard
    )        

    recify_image = Node(
        package='image_proc',
        executable='rectify_node',
        name='rectify_node',
        remappings=[
            ('image', '/image_raw')
        ],
        parameters=[{'image_transport': 'raw'}]
    )

    apriltag = Node(
        package='apriltag_ros',
        executable='apriltag_node',
        name='apriltag',
        remappings=[
            ('image_rect', '/image_rect')
        ],
       parameters=[apriltag_file]
    )

    upper_tag_2_world = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='upper_tag_st',
        output='screen',
        arguments=['3.7401', '0.0', '0.2921', '0.0', '0.0', '0.0', 'tag_upper', 'world_1']
    )

    lower_tag_2_world = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='lower_tag_st',
        output='screen',
        arguments=['-3.7401', '0.0', '0.2921', '0.0', '0.0', '0.0', 'tag_lower', 'world_2']
    )

    right_tag_2_world = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='right_tag_st',
        output='screen',
        arguments=['0', '3.7401', '0.2921', '0.0', '0.0', '0.0', 'tag_right', 'world_3']
    )

    left_tag_2_world = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='left_tag_st',
        output='screen',
        arguments=['0.0', '-3.7401', '0.2921', '0.0', '0.0', '0.0', 'tag_left', 'world_4']
    )

    # ros2 run tf2_ros static_transform_publisher x y z r p y parent_frame child_frame
    # ros2 run image_proc rectify_node --ros-args  --remap image:=/image_raw -p image_transport:=compressed
    # ros2 run apriltag_ros apriltag_node --ros-args --remap /image_rect:=/image_raw -p image_transport:=compressed
    
    return LaunchDescription([
        camera_node, 
        recify_image,
        apriltag,
        upper_tag_2_world,
        lower_tag_2_world,
        # right_tag_2_world,
        # left_tag_2_world
        ])
