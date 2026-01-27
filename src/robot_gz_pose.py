import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseArray, Pose, PoseWithCovarianceStamped, PoseStamped
from scipy.spatial.transform import Rotation as R

class RobotPose(Node):
    '''A node focused on cleaning up the ground truth information taken in from gazebo/ april tags'''
    def __init__(self):
        super().__init__("robot_pose")
        self.log = self.get_logger.info

        # import parameters
        self.declare_parameters(
          namespace='',
          parameters=[
              ('ground_truth_topic', '/ground_truth')
          ]
        )

        self.gt_topic = self.get_parameter('ground_truth_topic')

        # ground truth 
        self.ground_truth_listener = self.create_subscription(PoseArray, self.gt_topic, self.get_ground_truth, 10) # need GZ to ROS bridge for robot pose
        self.ground_truth = self.create_publisher(Pose, '/robot_pose', 10)

        # IMU
        # self.imu_pose = self.create_subscription(IDKWhatMsgType, '/imu', self.imu_pose)

        # robot localization pkg
        # self.robot_localization = ...

        # VEX odom from hardware interface?
        # self.robot_localization = ...

        # omni wheel controller?
        # self.controller_pose = ...
    
    def get_ground_truth(self, sim_robot:PoseArray) -> PoseStamped:
        '''get gazebo sim ground truth, simplify it, and publish to topic '/robot_pose'''
        robot_pos = sim_robot[1].position
        robot_rot = sim_robot[1].orientation

        robot = PoseStamped()
        robot.position = robot_pos
        robot.orientation = robot_rot

        self.ground_truth.publish(robot)

def main(args=None):
    rclpy.init(args=args)
    node = RobotPose()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()  