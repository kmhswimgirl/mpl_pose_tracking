#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_pose_error(csv_file):
    '''calculate error between ground truth and amcl'''
   
    df = pd.read_csv(csv_file)
   
    df['error_x'] = df['amcl_x'] - df['robot_x']
    df['error_y'] = df['amcl_y'] - df['robot_y']
    
    # euclidean distance
    df['error_distance'] = np.sqrt(df['error_x']**2 + df['error_y']**2)
    
    # rotation error + normalization
    angle_diff = df['amcl_r'] - df['robot_r']
    df['error_r'] = np.arctan2(np.sin(angle_diff), np.cos(angle_diff))
    
    return df

def plot_errors(df, output_dir=None, csv_file=None):
    '''plot pose errors from AMCL'''
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # stats
    mean_pos_error = df['error_distance'].mean()
    max_pos_error = df['error_distance'].max()
    mean_rot_error = np.abs(df['error_r']).mean()
    max_rot_error = np.abs(df['error_r']).max()
    
    stats_text = (
        f"Position Error Statistics:\n"
        f"  Mean: {mean_pos_error:.4f} m\n"
        f"  Max: {max_pos_error:.4f} m\n\n"
        f"Rotation Error Statistics:\n"
        f"  Mean: {mean_rot_error:.4f} rad ({np.degrees(mean_rot_error):.2f}°)\n"
        f"  Max: {max_rot_error:.4f} rad ({np.degrees(max_rot_error):.2f}°)"
    )
    
    # position over time
    axes[0].plot(df.index, df['error_distance'], label='Distance Error', color='red')
    axes[0].set_xlabel('Sample')
    axes[0].set_ylabel('Position Error (m)')
    axes[0].set_title('AMCL Position Error Over Time')
    axes[0].grid(True)
    axes[0].legend()
    
    # rotation error over time 
    axes[1].plot(df.index, np.degrees(df['error_r']), label='Rotation Error', color='blue')
    axes[1].set_xlabel('Sample')
    axes[1].set_ylabel('Rotation Error (degrees)')
    axes[1].set_title('AMCL Rotation Error Over Time')
    axes[1].grid(True)
    axes[1].legend()
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    fig.text(0.02, 0.5, stats_text, fontsize=10, verticalalignment='center',
             bbox=props, family='monospace')
    
    if csv_file:
            filename = os.path.basename(csv_file)
            fig.text(0.01, 0.01, f'Source: {filename}', fontsize=6, 
                    color='gray', alpha=0.7, family='monospace')
        
    plt.tight_layout()
    plt.subplots_adjust(left=0.25) 
    
    if output_dir:
        plt.savefig(os.path.join(output_dir, f'pose_errors.png'), bbox_inches='tight')
        print(f"Saved error plot to {output_dir}/pose_errors.png")
    
    plt.show()

def main():
    csv_file = '' # input csv file
    
    df_with_errors = calculate_pose_error(csv_file)
    
    output_dir = os.path.dirname(csv_file)
    plot_errors(df_with_errors, output_dir, csv_file)
    
    # make updated CSV for later
    output_csv = csv_file.replace('.csv', '_with_errors.csv')
    df_with_errors.to_csv(output_csv, index=False)
    print(f"\nSaved data with errors to {output_csv}")

if __name__ == '__main__':
    main()