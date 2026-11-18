import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    package_dir = get_package_share_directory('loader_simulation')

    world = os.path.join(
        package_dir,
        'worlds',
        'empty_world.sdf'
    )

    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                gazebo_ros_dir,
                'launch',
                'gzserver.launch.py'
            )
        ),
        launch_arguments={'world': world}.items()
    )

    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                gazebo_ros_dir,
                'launch',
                'gzclient.launch.py'
            )
        )
    )

    return LaunchDescription([
        gzserver
    ])