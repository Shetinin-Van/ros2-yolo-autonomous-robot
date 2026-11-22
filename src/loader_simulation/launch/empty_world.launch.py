import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    AppendEnvironmentVariable
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    pkg_simulation = get_package_share_directory('loader_simulation')
    pkg_description = get_package_share_directory('loader_description')

    world = os.path.join(pkg_simulation, 'worlds', 'empty_world.sdf')

    xacro_file = os.path.join(pkg_description, 'urdf', 'wheel_loader.urdf.xacro')
    doc = xacro.process_file(xacro_file, mappings={'sim': 'classic'})
    robot_desc = doc.toprettyxml(indent='  ')

    gazebo_model_path = AppendEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=os.path.join(pkg_simulation, 'models') + ':' + os.path.join(pkg_description, 'meshes')
    )

    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gzclient.launch.py')
        )
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}],
        output='screen'
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_loader', '-z', '1.0'],
        output='screen'
    )

    spawn_joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen'
    )

    return LaunchDescription([
        gazebo_model_path,
        gzserver,
        gzclient,
        robot_state_publisher,
        spawn_entity,
        spawn_joint_state_broadcaster
    ])
