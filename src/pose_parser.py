#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseArray, TwistStamped
import pandas as pd
from scipy.spatial.transform import Rotation as R
import numpy as np
import os
from datetime import datetime

class PoseParser(Node):
    def __init__(self):
        super().__init__('pose_parser')
        
        # subscribers
        self.amcl_sub = self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.amcl_callback, 10)
        self.robot_sub = self.create_subscription(PoseArray, '/otto_pose', self.robot_callback, 10)
        self.cmd_vel = self.create_subscription(TwistStamped, '/cmd_vel', self.velocity_callback, 10)

        # self.frequency = self.create_timer(0.5, self.plot_data)
        
        # data structure
        self.data = {
            'amcl_x': [],
            'amcl_y': [],
            'amcl_r': [],
            'robot_x': [],
            'robot_y': [],
            'robot_r': [],
            'cmd_vel_x': [],
            'cmd_vel_y': [],
            'cmd_vel_r': []
        }
        
        self.robot_x = None
        self.robot_y = None
        self.robot_r = None
        
        self.cmd_vel_y = None
        self.cmd_vel_x = None
        self.cmd_vel_r = None

        # uniquely named file (.csv)
        workspace_path = '/home/kymadogg/ros2_ws/src/mqp/mpl_pose_tracking/data'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.csv_name = os.path.join(workspace_path, 'nav2_data', f'poses_{timestamp}.csv')
        
        self.get_logger().info(f"PoseParser node initialized. Output file: {self.csv_name}")
    
    def robot_callback(self, msg: PoseArray):
        '''update current robot pose'''
        if len(msg.poses) > 0:
            self.robot_x = msg.poses[-1].position.x
            self.robot_y = msg.poses[-1].position.y

            quat = msg.poses[-1].orientation
            quat_array = np.array([quat.x, quat.y, quat.z, quat.w])

            # normalize
            quat_norm = np.linalg.norm(quat_array)
            if quat_norm > 0: 
                quat_normalized = quat_array / quat_norm
            else:
                quat_normalized = quat_array 
                
            rotation = R.from_quat(quat_normalized)

            euler = rotation.as_euler('xyz') # THIS IS IN RADIANS!
            self.robot_r = euler[2] # get the yaw (z rotation) value from the returned array

    def velocity_callback(self, msg:TwistStamped):
        '''record current velocity'''
        self.cmd_vel_x = msg.twist.linear.x
        self.cmd_vel_y = msg.twist.linear.y
        self.cmd_vel_r = msg.twist.angular.z

    def amcl_callback(self, msg: PoseWithCovarianceStamped):
        '''keep record on AMCL poses'''
        self.amcl_x = msg.pose.pose.position.x
        self.amcl_y = msg.pose.pose.position.y

        quat = msg.pose.pose.orientation
        quat_array = np.array([quat.x, quat.y, quat.z, quat.w])

        # normalize
        quat_norm = np.linalg.norm(quat_array)
        if quat_norm > 0: 
            quat_normalized = quat_array / quat_norm
        else:
            quat_normalized = quat_array 
            
        rotation = R.from_quat(quat_normalized)

        euler = rotation.as_euler('xyz') # THIS IS IN RADIANS!
        self.amcl_r = euler[2] # get the yaw (z rotation) value from the returned array

        self.plot_data()

    def plot_data(self):

        if (self.robot_x is None or self.robot_y is None or self.robot_r is None or
            self.cmd_vel_x is None or self.cmd_vel_y is None or self.cmd_vel_r is None):
            self.get_logger().debug("Waiting for all topics to publish data...")
            return
        
        '''record data in the data frame every 0.5s'''
        self.data['amcl_x'].append(self.amcl_x)
        self.data['amcl_y'].append(self.amcl_y)
        self.data['amcl_r'].append(self.amcl_r)
        self.data['robot_x'].append(self.robot_x)
        self.data['robot_y'].append(self.robot_y)
        self.data['robot_r'].append(self.robot_r)
        self.data['cmd_vel_x'].append(self.cmd_vel_x)
        self.data['cmd_vel_y'].append(self.cmd_vel_y)
        self.data['cmd_vel_r'].append(self.cmd_vel_r)
    
    def save_data(self):
        df = pd.DataFrame(self.data)
        df.to_csv(self.csv_name, index=False)
        self.get_logger().info(f"Saved {len(df)} poses to {self.csv_name}")

def main(args=None):
    rclpy.init(args=args)
    node = PoseParser()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Ending node...")
    finally:
        node.save_data()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()