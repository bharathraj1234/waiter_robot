#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    # Packages
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    waiter_dir = get_package_share_directory('waiter_robot')

    # Files
    map_file = os.path.join(waiter_dir, 'maps', 'map.yaml')
    rviz_config = os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')

    # ---------------- NAV2 ---------------- #
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_file,
            'use_sim_time': 'true',
            'autostart': 'true'
        }.items()
    )

    # ---------------- RVIZ ---------------- #
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([
        nav2,
        rviz
    ])
