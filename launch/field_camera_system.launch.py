#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python import get_package_share_directory


def generate_launch_description():
    pkg_dir= get_package_share_directory('mpl_pose_tracking')
    config_file = os.path.join(pkg_dir, 'config', 'camera_extended.yaml')

    camera_node =  Node( # launches
            package='usb_cam', 
            executable='usb_cam_node_exe', 
            output='screen',
            name='camera_1',
            parameters=[config_file] # camera calibration is still messed up
        )        
    
    recify_image = Node ( # untested
        package='image_proc',
        executable='rectify_node',
        arguments=[{'-r': 'image:=/image_raw'}],
        parameters=['image_transport', 'compressed']
    )
    # ros2 run image_proc rectify_node --ros-args  --remap image:=/image_raw -p image_transport:=compressed
    # ros2 run apriltag_ros apriltag_node --ros-args --remap /image_rect:=/image_raw -p image_transport:=compressed

    
    return LaunchDescription([camera_node])
