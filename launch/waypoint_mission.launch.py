from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            output='screen'
        ),
        Node(
            package='altair_phase3',
            executable='waypoint_mission',
            name='waypoint_mission',
            output='screen'
        ),
    ])
