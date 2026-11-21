import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    pkg_simulation = get_package_share_directory('loader_simulation')
    pkg_description = get_package_share_directory('loader_description')

    world_file = os.path.join(pkg_simulation, 'worlds','empty_world.sdf')
    xacro_file = os.path.join(pkg_description, 'urdf', 'wheel_loader.urdf.xacro')
    doc = xacro.process_file(xacro_file, mappings={'sim': 'classic'})
    robot_desc = doc.toprettyxml(indent='  ')
    
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
            launch_arguments={'world':world_file,'gui': 'true'}.items()
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_desc, 'use_sim_time': True}],
            output='screen'
        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'my_loader', '-z', '0.5'],
            output='screen'  
        )

    ]) 

