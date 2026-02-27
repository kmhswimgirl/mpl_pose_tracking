#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TransformStamped
from scipy.spatial.transform import Rotation as R
from tf2_geometry_msgs import PoseStamped
from apriltag_msgs.msg import AprilTagDetectionArray
from tf2_ros.transform_listener import TransformListener
from tf2_ros.transform_broadcaster import TransformBroadcaster
from tf2_ros.buffer import Buffer
from typing import List

'''
apriltag_ground_truth Node TF Tree
               +------------------+                   
               |robot ground truth| 
               |  (robot_tag)     | 
               +---------^--------+                   
                         |                            
               +---------+--------+                   
               |average world tf  |                   
               +---------^--------+                   
                         |                            
              +-------------------+                   
    +---------+ field camera frame+-------------+     
    |         | (root frame)      |             |     
    |         +----+-------------++             |     
    |              |             |              |     
+---v-----+   +----v----+     +--v------+   +---v----+
|upper tag|   |lower tag|     |right tag|   |left tag|
+---+-----+   +----+----+     +--+------+   +--+-----+
    |              |             |             |      
+---v---+     +----v--+       +--v----+     +--v----+ 
|world 1|     |world 2|       |world 3|     |world 4| 
+-------+     +-------+       +-------+     +-------+ 
'''

class RobotGroundTruth(Node):
    def __init__(self):
        super().__init__('apriltag_ground_truth')

        # apriltag detection subscriber
        self.ground_truth = self.create_subscription(AprilTagDetectionArray, '/detections', self.apriltag_callback, 10)

        # tf listener/buffer
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # world frame tf publisher
        self.tf_broadcaster = TransformBroadcaster(self)

        # robot ground truth publisher
        self.robot_ground_truth = self.create_publisher(PoseStamped, '/robot_ground_truth', 10)

        self.robot_frame = 'robot_tag' # robot apriltag (ID 0) frame name

    def apriltag_callback(self, msg:AprilTagDetectionArray):
        '''callback function for when apriltag detections are published on /detections'''
        
        self.get_average_world_frame()
        self.publish_robot_ground_truth()

    def average_transforms(self, transforms:List[TransformStamped]):
        '''average a list of transforms'''
        xs, ys, zs = [], [], []
        quats = []
        for tf in transforms:
            t = tf.transform.translation
            xs.append(t.x)
            ys.append(t.y)
            zs.append(t.z)
            r = tf.transform.rotation
            quats.append([r.x, r.y, r.z, r.w])
        avg_translation = [sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs)]

        rot = R.from_quat(quats)
        avg_rot = rot.mean()
        avg_quat = avg_rot.as_quat() 

        return avg_translation, avg_quat
    
    def get_frame_tf(self, target_frame, source_frame):
        '''get the transform between the target and source frames'''
        try:
            trans = self.tf_buffer.lookup_transform(
                target_frame, # child frame
                source_frame, # parent frame
                rclpy.time.Time() # get most recent transform
            )
            return trans
        except Exception as ex:
            self.get_logger().warn(f"no available TF {source_frame} to {target_frame}: {ex}")
            return None

    def get_average_world_frame(self): 
        '''average world frames w.r.t. the camera frame and publish a new frame representing the average world frame'''

        w1_to_cam = self.get_frame_tf("field_cam", "world_1")
        w2_to_cam = self.get_frame_tf("field_cam", "world_2")
        w3_to_cam = self.get_frame_tf("field_cam", "world_3")
        w4_to_cam = self.get_frame_tf("field_cam", "world_4")

        # none handling
        transforms = [w1_to_cam, w2_to_cam, w3_to_cam, w4_to_cam]
        valid_transforms = [tf for tf in transforms if tf is not None]

        if len(valid_transforms) == 0:
            self.get_logger().warn("no valid world transforms available")
            return

        avg_trans, avg_quat = self.average_transforms(valid_transforms)

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'field_cam'
        t.child_frame_id = 'world_frame'
        t.transform.translation.x = avg_trans[0]
        t.transform.translation.y = avg_trans[1]
        t.transform.translation.z = avg_trans[2]
        t.transform.rotation.x = avg_quat[0]
        t.transform.rotation.y = avg_quat[1]
        t.transform.rotation.z = avg_quat[2]
        t.transform.rotation.w = avg_quat[3]


        self.tf_broadcaster.sendTransform(t)

    def publish_robot_ground_truth(self): 
        ''' find the frame difference and publish the ground truth to a topic'''

        robot_tf = self.get_frame_tf(self.robot_frame, "world_frame")

        # error handling if no robot pose
        if robot_tf is None:
            self.get_logger().warn("robot frame not available for publishing ground truth")
            return

        # TransformStamped --> PoseStamped
        pose = PoseStamped()
        pose.header = robot_tf.header
        pose.header.frame_id = robot_tf.child_frame_id
        pose.pose.position.x = robot_tf.transform.translation.x
        pose.pose.position.y = robot_tf.transform.translation.y
        pose.pose.position.z = robot_tf.transform.translation.z
        pose.pose.orientation = robot_tf.transform.rotation
        
        self.robot_ground_truth.publish(pose)

def main(args=None):
    rclpy.init(args=args)
    node = RobotGroundTruth()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
            node.destroy_node()
            rclpy.shutdown()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()