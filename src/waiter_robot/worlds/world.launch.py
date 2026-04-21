from launch import LaunchDescription
from launch.actions import ExecuteProcess
import os

def generate_launch_description():

    world = os.path.join(
        os.path.dirname(__file__),
        '..',
        'worlds',
        'restaurant.world'
    )

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world],
            output='screen'
        )
    ])
