"""
디버그 런치 — YOLO 없이 라인트레이싱 + 키보드 표지판으로 상태머신 테스트.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    camera_pkg = get_package_share_directory('camera_ros')
    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(camera_pkg, 'launch', 'camera.launch.py')
        )
    )

    lane_detector = Node(
        package='aicar_vision',
        executable='lane_detector_node',
        name='lane_detector_node',
        output='screen',
    )

    fake_detector = Node(
        package='aicar_vision',
        executable='fake_detector_node',
        name='fake_detector_node',
        output='screen',
        prefix='xterm -e',  # 별도 터미널에서 input 가능
    )

    controller = Node(
        package='aicar_controller',
        executable='driving_controller_node',
        name='driving_controller_node',
        output='screen',
        parameters=[{
            'vehicle_speed': 0.15,
            'skip_system_handshake': True,  # ⚠️ fake 모드라 handshake 건너뜀
        }],
    )

    motor = Node(
        package='aicar_driver',
        executable='differential_drive_node',
        name='differential_drive_node',
        output='screen',
    )

    return LaunchDescription([
        camera_launch,
        lane_detector,
        fake_detector,
        controller,
        motor,
    ])
