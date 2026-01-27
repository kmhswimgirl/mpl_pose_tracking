import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import csv

field_side = 3.66

def base_plot():
    fig, ax = plt.subplots()
    # ax.set_title("VEX 12x12 ft Competition Field")

    ax.set_xlim(0, field_side)
    ax.set_ylim(0, field_side)
    ax.set_aspect('equal', adjustable='box')

    ticks = [field_side/3, 2*field_side/3, field_side]
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    show_field_elements(ax)

    ax.grid(True)
    # plt.show()

def transform_coords_center(x, y, xw, yh):
    field = 3.66
    c = field / 2
    mx =  y + c - (xw/2)
    my = -x + c - (yh/2)
    return (mx, my)

def translate_point(num):
    center_offset = field_side / 2
    new_num = num + center_offset
    return new_num

def show_field_elements(ax):
    '''plotting the base VEX field dimensions'''
    center = field_side / 2

    # center goal
    center_goal = patches.Rectangle((center - 0.25, center - 0.25),0.5, 0.5, linewidth=2, edgecolor='gray', facecolor='lightgray')
    ax.add_patch(center_goal)

    # add loaders
    loaders = [(1.19, -1.72), (-1.19, -1.72), (-1.19, 1.72), (1.199, 1.72)]
    for loader in loaders:
        loader_c = transform_coords_center(loader[0], loader[1], 0.20, 0.20)
        loader = patches.Rectangle(loader_c, 0.20, 0.20, linewidth=2, edgecolor='gray', facecolor='lightgray')
        ax.add_patch(loader)

    # long goals
    long_goals = [(-1.20, 0), (1.20, 0)]
    for goal in long_goals:
        goal_coords = transform_coords_center(goal[0], goal[1], 1.239, 0.20)
        goals = patches.Rectangle(goal_coords, 1.239, 0.20, linewidth=2, edgecolor='gray', facecolor='lightgray')
        ax.add_patch(goals)

    # park_zones = [(0, 1.44), (0, -1.44)]
    # for zone in park_zones:
    #     zone_coords = transform_coords_center(zone[0], zone[1], 0.32, 0.32)
    #     zones = patches.Rectangle(zone_coords, 0.32, 0.32, linewidth=4, edgecolor='gray', facecolor='white')
    #     ax.add_patch(zones)

def add_start_marker(x, y, color='green', label='Start'):
    x_pt = translate_point(x)
    y_pt = translate_point(y)
    plt.plot(x_pt, y_pt, marker='X', color=color, markersize=12, label=label, markeredgewidth=2, markeredgecolor='black')
    plt.legend()


def add_robot_path(data_file, color, label, x_col=0, y_col=1):
    x = []
    y = []
    with open(data_file, 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            if len(row) > max(x_col, y_col):
                try:
                    x_pt = translate_point(float(row[x_col]))
                    y_pt = translate_point(float(row[y_col]))
                    x.append(x_pt)
                    y.append(y_pt)
                except ValueError:
                    continue  # Skip header or invalid rows

    plt.plot(x, y, color=color, label=label, marker='o', markersize=2)
    plt.legend()

# what is executed
base_plot()
# Column 0,1 for amcl_x, amcl_y or 2,3 for robot_x, robot_y
add_robot_path('data/amcl_data/poses_2.csv', 'red', '/amcl_pose', x_col=0, y_col=1)
print('done')
add_robot_path('data/amcl_data/poses_2.csv', 'blue', '/ground_truth', x_col=2, y_col=3)
print('done x2')
add_start_marker(0.5, 0.5, 'green', 'Start Position')
plt.show()