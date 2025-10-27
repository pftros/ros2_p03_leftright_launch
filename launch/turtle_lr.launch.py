from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """
    Generates the launch description for starting turtlesim and the controller.
    """
    return LaunchDescription([
        # Start the turtlesim node
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'  # Name this node 'sim'
        ),
        
        # Start the turtle_lr node from py_subsub package
        Node(
            package='py_pubsub',
            executable='turtle_lr_node',
            name='controller', # Name this node 'controller'
            remappings=[
                # Remap the node's 'cmd_vel' topic to '/turtle1/cmd_vel'
                ('cmd_vel', '/turtle1/cmd_vel'),
                # Remap the node's 'pose' topic to '/turtle1/pose'
                ('pose', '/turtle1/pose')
            ]
            # The --ros-args are handled implicitly by the remappings parameter.
        ),
    ])

