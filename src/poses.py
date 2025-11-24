import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose
from apriltag_msgs.msg import AprilTagDetectionArray, AprilTagDetection

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

        self.log = self.get_logger.info

        # Apriltag IDs
        self.robot_id = 20
        self.origin_id = 0
        self.corners_id = [4,6,8]
        self.opponent_id = 1

        # sim vs real toggle point
        self.simulated = False

        # ground truth subscriber
        if self.simulated:
            self.ground_truth = self.create_subscription(Pose,'/')
        else:
            self.ground_truth = self.create_subscription(AprilTagDetectionArray, '/detections')

        # IMU
        # robot localization
        # AMCL
        # VEX odom?
        # omni wheel controller

    def calculate_ground_truth(self, msg:AprilTagDetectionArray):
        '''Take in april tag data and figure out where the robot is'''
        self.log("getting data from Apriltags...")
        tags = msg
        for tag in tags:
            if tag.id == self.origin_id:
                tag.pose

        

    
        

