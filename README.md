# mpl_pose_tracking
Data collection and pose tracking packages for autonomous robots.

Originally made to work with the otto packages in `Autonomous-VEXU`.

## Launch Files
There are a few launch files for various different types of pose tracking. Working on implementing all of the parameters in a YAML file for simplicity.

### `sim_pose_tracking.launch.py`
TLDR: Launches a gazebo VEX field + robot + amcl + optional teleop & rosbag recording</br>

**Launch Arguments:**
- `teleop`: toggles the launching of the teleop control nodes on or off (default: True)
- `bridge_name`: the name that the gazebo bridge will inherit
- `config_file`: the config file passed to the gazebo bridge node
- `rosbag`: toggles recording a rosbag on or off (default: False)

## Nodes
TBD

## Scripts
A few non-node python files that can generate graphs or filter rosbag data.

### `field_plotter.py`
Takes in multiple CSV files and plots them on a matplotlib graph that represents the VEX field.
