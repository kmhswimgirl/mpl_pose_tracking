
import rclpy
import math
from rclpy.node import Node
from nav_msgs.msg import Odometry
from nav_msgs.srv import GetPlan
from geometry_msgs.msg import TwistStamped, PoseStamped, Pose
from scipy.spatial.transform import Rotation as R
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from tf2_geometry_msgs import PoseStamped
from apriltag_msgs.msg import AprilTagDetectionArray, AprilTagDetection

from tf2_ros.transform_listener import TransformListener
from tf2_ros.buffer import Buffer

'''
kymadogg@kh-fw-16:~$ ros2 interface show apriltag_msgs/msg/AprilTagDetectionArray
std_msgs/Header header
	builtin_interfaces/Time stamp
		int32 sec
		uint32 nanosec
	string frame_id
AprilTagDetection[] detections
	string family
	int32 id
	int32 hamming
	float32 goodness
	float32 decision_margin
	Point centre                    #
		float64 x
		float64 y
	Point[4] corners                #
		float64 x
		float64 y
	float64[9] homography           #
'''

class PoseTracker(Node):
    def __init__(self):
        self.declare_parameters(
            namespace='',
            parameters=[
                ('origin_id', 32),
                ('robot_id', 5)
            ])
        self.log = self.get_logger.info

        # Apriltag IDs
        self.robot_id = self.get_parameter('robot_id').value
        self.origin_id = self.get_parameter('origin_id').value
        # self.corners_id = [4,6,8]
        # self.opponent_id = 1

        # ground truth subscriber
        self.ground_truth = self.create_subscription(AprilTagDetectionArray, '/detections', self.calculate_ground_truth)

        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self)

        # IMU
        # robot localization
        # AMCL
        # VEX odom?
        # omni wheel controller

    def get_relative_coords(self):
        
        
        pass

    def calculate_ground_truth(self, msg:AprilTagDetectionArray):
        '''Take in april tag data and figure out where the robot is'''
        self.log("getting data from Apriltags...")
        tags = msg
        for tag in tags:
            if tag.id == self.origin_id:
                pass