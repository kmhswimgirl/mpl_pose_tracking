#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseArray
import pandas as pd
import os
from datetime import datetime

class DetailedPlotter(Node):
    def __init__(self):
        super().__init__('detailed_plotter')
        
        # subscribers
        self.amcl_sub = self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.amcl_callback, 10)
        self.robot_sub = self.create_subscription(PoseArray, '/otto_pose', self.robot_callback, 10)
        
        # data storage
        self.data = {
            'amcl_x': [],
            'amcl_y': [],
            'robot_x': [],
            'robot_y': []
        }
        
        self.robot_x = None
        self.robot_y = None
        
        # Output file with unique timestamp
        workspace_path = '/home/kymadogg/ros2_ws/src/mqp/mpl_pose_tracking/data'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.csv_name = os.path.join(workspace_path, 'nav2_data', f'detailed_poses_{timestamp}.csv')
        
        self.get_logger().info(f"DetailedPlotter initialized. Output: {self.csv_name}")
    
    def robot_callback(self, msg: PoseArray):
        '''update current robot pose'''
        if len(msg.poses) > 0:
            self.robot_x = msg.poses[-1].position.x
            self.robot_y = msg.poses[-1].position.y
    
    def amcl_callback(self, msg: PoseWithCovarianceStamped):
        '''record AMCL and robot poses together'''
        if self.robot_x is not None and self.robot_y is not None:
            amcl_x = msg.pose.pose.position.x
            amcl_y = msg.pose.pose.position.y
            
            self.data['amcl_x'].append(amcl_x)
            self.data['amcl_y'].append(amcl_y)
            self.data['robot_x'].append(self.robot_x)
            self.data['robot_y'].append(self.robot_y)
            
            if len(self.data['amcl_x']) % 50 == 0:
                self.get_logger().info(f"Recorded {len(self.data['amcl_x'])} pose pairs")
    
    def save_data(self):
        df = pd.DataFrame(self.data)
        df.to_csv(self.csv_name, index=False)
        self.get_logger().info(f"Saved {len(df)} poses to {self.csv_name}")

def main(args=None):
    rclpy.init(args=args)
    node = DetailedPlotter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.save_data()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()