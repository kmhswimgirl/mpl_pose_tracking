
import rclpy
import math
from rclpy.node import Node
from nav_msgs.msg import Odometry
from nav_msgs.srv import GetPlan
from geometry_msgs.msg import TwistStamped, PoseStamped, Pose, TransformStamped
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
	Point centre                    
		float64 x
		float64 y
	Point[4] corners                
		float64 x
		float64 y
	float64[9] homography           
'''

class PoseTracker(Node):
    def __init__(self):
        super().__init__('apriltag_ground_truth')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('robot_id', 0),
                ('field_tags', (11, 22, 33, 44))  # clockwise from 
            ]
        )
        self.log = self.get_logger.info

        # Apriltag IDs
        self.robot_id = self.get_parameter('robot_id').value
        self.field_tags = self.get_parameter('field_tags').value

        # apriltag detection subscriber
        self.ground_truth = self.create_subscription(AprilTagDetectionArray, '/detections', self.apriltag_callback)

        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self)

        self.target_frame = 'frame1' # Replace with your first frame ID
        self.source_frame = 'frame2' # Replace with your second frame ID

        self.timer = self.create_timer(1.0, self.on_timer) 

    def get_relative_coords(self):
        

        
        pass

    def apriltag_callback(self, msg:AprilTagDetectionArray):
        '''populate the global tag coordinates'''
        self.log("getting data from Apriltags...")
        tags = msg