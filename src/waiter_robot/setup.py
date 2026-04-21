from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'waiter_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # ROS package index
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),

        # Package.xml
        ('share/' + package_name, ['package.xml']),

        # Launch files
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),

        # World files
        (os.path.join('share', package_name, 'worlds'),
            glob('worlds/*.world')),

        # 🔥 ADD THIS → MAP FILES
        (os.path.join('share', package_name, 'maps'),
            glob('maps/*')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bharathraj',
    maintainer_email='bharathraj@todo.todo',
    description='Waiter robot simulation using ROS2 and Gazebo',
    license='Apache License 2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'main=waiter_robot.main:main'
        ],
    },
)
