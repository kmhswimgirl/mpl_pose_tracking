import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

field_side = 3.66

def base_plot():
    fig, ax = plt.subplots()
    ax.set_title("VEX 12x12 ft Competition Field")

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

    center_goal = patches.Rectangle((center - 0.25, center - 0.25),0.5, 0.5, linewidth=2, edgecolor='black', facecolor='gray')
    ax.add_patch(center_goal)

    # add loaders
    loaders = []
    for loader in loaders:
        loader_c1 = transform_coords_center(1.19, -1.72, 0.25, 0.25)
        loader_1 = patches.Rectangle(loader_c1, 0.25, 0.25, linewidth=2, edgecolor='black', facecolor='gray')
        ax.add_patch(loader_1)


base_plot()
