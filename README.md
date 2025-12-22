# mpl_pose_tracking
Data collection and pose tracking packages for autonomous robots.

Originally made to work with the otto packages in `Autonomous-VEXU`.

## Launch Files
There are a few launch files for various different types of pose tracking

launch arguments are listed in the following format:
```
Launch Argument | default value : description
```

## `sim_pose_tracking.launch.py`
Arguments:
- `teleop`: toggles the launching of the teleop control nodes on or off (default: True)
- `bridge_name`: the name that the gazebo bridge will inherit
- `config_file`: the config file passed to the gazebo bridge node
- `rosbag`: toggles recording a rosbag on or off (default: False)

## Nodes
TBD