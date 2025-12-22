
import rclpy
import math
from datetime import datetime
import pandas as pd # type: ignore
from rclpy.node import Node
from geometry_msgs.msg import PoseArray, Pose, PoseWithCovarianceStamped
from scipy.spatial.transform import Rotation as R

from tf2_ros.transform_listener import TransformListener
from tf2_ros.buffer import Buffer

class PoseTracker(Node):
  
    def __init__(self):
        super().__init__("pose_tracker")
        self.log = self.get_logger.info

        # import parameters
        self.declare_parameters(
          namespace='',
          parameters=[
            ('collect_data', True),
            ('amcl_topic', '/amcl_pose')
            ('ground_truth_topic', '/world/default/dynamic_pose/info'),
            ('log_file_prefix', 'robot_data')
          ]
        )

        # data storage for csv export
        self.data = []

        # ground truth subscriber
        self.ground_truth = self.create_subscription(PoseArray, '/world/default/dynamic_pose/info', self.get_ground_truth, 10) # need GZ to ROS bridge for robot pose

        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self)

        # AMCL
        if self.amcl_topic is not None:
          self.amcl_pose = self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.amcl_pose_calc )

        # IMU
        # self.imu_pose = self.create_subscription(IDKWhatMsgType, '/imu', self.imu_pose)

        # robot localization pkg
        # self.robot_localization = ...

        # VEX odom from hardware interface?
        # self.robot_localization = ...

        # omni wheel controller?
        # self.controller_pose = ...

        self.add_on_shutdown(self.save_to_csv)
    

    def get_ground_truth(self, sim_robot:PoseArray):
        '''get gazebo sim ground truth and either store or plot it'''
        robot_x = sim_robot[0].position.x
        robot_y = sim_robot[0].position.y

        robot_coords = (robot_x, robot_y)
        self.data.append({'x': robot_x, 'y': robot_y})
        self.log(f'Robot Gazebo Coordinates: {robot_coords}')
    
    def get_amcl_pose(self, amcl_pose:PoseWithCovarianceStamped):
        amcl_x = amcl_pose.pose.pose.position.x 
        amcl_y = amcl_pose.pose.pose.position.y

        amcl_coords = (amcl_x, amcl_y)
    
    def main_loop(self):
        pass
        
    @staticmethod
    def append_to_data(self):
      pass

    def save_to_csv(self):
        df = pd.DataFrame(self.data)
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        df.to_csv(f'robot_data_{timestamp}.csv', index=False)
        self.log("Saved ground truth data to ground_truth_log.csv")


        