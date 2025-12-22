import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

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
    plt.show()

def transform_coords_center(x, y, xw, yh):
    field = 3.66
    c = field / 2
    mx =  y + c - (xw/2)
    my = -x + c - (yh/2)
    return (mx, my)

def show_field_elements(ax):
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
    
base_plot()