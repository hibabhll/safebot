from setuptools import setup
from glob import glob
import os

package_name = 'robot_safety'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hiba', maintainer_email='hiba@todo.todo',
    description='Robot Safety Monitor', license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'sensor_simulator = robot_safety.sensor_simulator:main',
            'health_monitor = robot_safety.health_monitor:main',
            'safety_controller = robot_safety.safety_controller:main',
            'terminal_dashboard = robot_safety.terminal_dashboard:main',
            'data_logger = robot_safety.data_logger:main',
        ],
    },
)
