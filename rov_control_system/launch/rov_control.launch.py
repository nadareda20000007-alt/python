import os
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # 1. Joy Node (Reads physical controller input and publishes /joy)
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        output='screen',
        parameters=[{
            'dev': '/dev/input/js0',      # Path to your connected joystick/gamepad device
            'deadzone': 0.05,             # Hardware-level deadzone
            'autorepeat_rate': 20.0,      # Publish rate (Hz) when stick is held still
        }],
        remappings=[
            ('/joy', '/joystick')          # Remaps standard /joy topic to your /joystick topic
        ]
    )

    # 2. Navigation Node (Your smoothing & safety pipeline)
    navigation_node = Node(
        package='rov_control_system',
        executable='navigation_node',
        name='navigation_node',
        output='screen',
    )

    return LaunchDescription([
        joy_node,
        navigation_node,
    ])