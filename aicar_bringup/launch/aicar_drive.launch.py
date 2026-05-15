import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # --- Args ---
    vehicle_speed = DeclareLaunchArgument(
        'vehicle_speed', default_value='0.20',
        description='Base linear speed [m/s]'
    )
    skip_handshake = DeclareLaunchArgument(
        'skip_handshake', default_value='false',
        description='If true, controller starts immediately without waiting for system_ready'
    )
    use_dashboard = DeclareLaunchArgument(
        'use_dashboard', default_value='true',
        description='Launch Tkinter dashboard UI'
    )

    # --- Camera (from camera_ros) ---
    camera_pkg = get_package_share_directory('camera_ros')
    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(camera_pkg, 'launch', 'camera.launch.py')
        )
    )

    # --- Vision ---
    lane_detector = Node(
        package='aicar_vision',
        executable='lane_detector_node',
        name='lane_detector_node',
        output='screen',
        parameters=[{'image_topic': '/camera_node/image_raw'}],
    )

    sign_detector = Node(
        package='aicar_vision',
        executable='sign_detector_node',
        name='sign_detector_node',
        output='screen',
        parameters=[{'image_topic': '/camera_node/image_raw'}],
    )

    # --- Controller ---
    controller = Node(
        package='aicar_controller',
        executable='driving_controller_node',
        name='driving_controller_node',
        output='screen',
        parameters=[{
            'vehicle_speed': LaunchConfiguration('vehicle_speed'),
            'skip_system_handshake': LaunchConfiguration('skip_handshake'),
        }],
    )

    # --- Motor driver ---
    motor = Node(
        package='aicar_driver',
        executable='differential_drive_node',
        name='differential_drive_node',
        output='screen',
    )

    # --- Dashboard (optional) ---
    dashboard = Node(
        package='aicar_ui',
        executable='dashboard_node',
        name='dashboard_node',
        output='screen',
        condition=IfCondition(LaunchConfiguration('use_dashboard')),
    )

    return LaunchDescription([
        vehicle_speed,
        skip_handshake,
        use_dashboard,
        camera_launch,
        lane_detector,
        sign_detector,
        controller,
        motor,
        dashboard,
    ])
