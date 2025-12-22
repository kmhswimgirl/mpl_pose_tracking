# mcap filter to get data for plotting using ros2 api
# (kind of) UNTESTED

import rclpy
from rclpy.node import Node
from rclpy.serialization import deserialize_message
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseArray

import os
import pandas as pd

def topic_parsing(input:str, topics: dict, output: str):
    rclpy.init()

    reader = SequentialReader()
    storage = StorageOptions(uri=input, storage_id='mcap')
    converter = ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')

    reader.open(storage, converter)

    data = {topic: [] for topic in topics}
    while reader.has_next():
        (topic, d_bytes,timestamp) = reader.read_next()

        if topic in topics:
            msg_type = topics[topic]
            msg = deserialize_message(d_bytes, msg_type)
            timestamp_s = timestamp / 1e9

            # amcl (PoseWithCovarianceStamped)
            if msg_type == PoseWithCovarianceStamped:
                pose = msg.pose.pose
                data[topic].append({ # only want x, y for now
                    'timestamp': timestamp_s,
                    'x': pose.position.x,
                    'y': pose.position.y
                })

            # robot sim ground truth (pose index 1 for robot)
            elif msg_type == PoseArray:
                for i, pose in enumerate(msg.poses):
                    if i == 1: # only want Otto's pose
                        data[topic].append({
                            'timestamp': timestamp_s,
                            'x': pose.position.x,
                            'y': pose.position.y
                        })
                        break # i think that makes sense here...
    reader.close()
    rclpy.shutdown()

    save_csv(output, data)

def save_csv(output:str, data:dict):
    try:
        os.makedirs(output,exist_ok =False) # prevent overwrites
    except: FileExistsError

    for topic, records in data.items():
        if records:
            df = pd.DataFrame(records)
            csv_file = os.path.join(output, f'{topic.replace('/','_')}.csv')
            df.to_csv(csv_file, index = False)
            print("saved file :)")

if __name__ == '__main__':
    topics = {
        '/amcl_pose' : PoseWithCovarianceStamped,
        '/ground_truth' : PoseArray
    }

    topic_parsing('', topics, '')
            