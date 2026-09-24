import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('robot_safety')
    params_file = os.path.join(pkg_share, 'config', 'health_monitor_params.yaml')

    return LaunchDescription([
        Node(package='robot_safety', executable='sensor_simulator', output='screen'),
        Node(package='robot_safety', executable='health_monitor',
             output='screen', parameters=[params_file]),
        Node(package='robot_safety', executable='safety_controller', output='screen'),
        Node(package='robot_safety', executable='terminal_dashboard', output='screen'),
        Node(package='robot_safety', executable='data_logger', output='screen'),
    ])
