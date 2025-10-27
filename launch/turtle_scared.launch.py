from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, TimerAction

def generate_launch_description():
    """
    Generates the launch description for starting:
    1. turtlesim
    2. The turtle_lr controller for turtle1 with a parameter.
    3. Spawning a second turtle (turtle2).
    4. Launching teleop_twist_keyboard for turtle2 in a new xterm.
    """
    
    # 1. Start the turtlesim node
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='sim'
    )
    
    # 2. Start the turtle_lr node from py_pubsub package
    controller_node = Node(
        package='py_pubsub',
        executable='turtle_lr_node',
        name='controller',
        parameters=[
            {'range': 0.0}  # Set the 'range' parameter
        ],
        remappings=[
            # Remap topics for turtle1
            ('cmd_vel', '/turtle1/cmd_vel'),
            ('pose', '/turtle2/pose')
        ]
    )
    
    # 3. Command to spawn turtle2
    spawn_turtle2_cmd = ExecuteProcess(
        # Note: The complex argument is passed as a single string.
        cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', 
             "{x: 2, y: 2, theta: 0.2, name: 'turtle2'}"],
        output='screen'
    )

    # 4. Run teleop_twist_keyboard for turtle2 in xterm
    teleop_turtle2_node = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_turtle2',
        prefix='xterm -e',  # Launch in a new xterm window
        remappings=[
            # Remap this node's cmd_vel to turtle2's cmd_vel
            ('cmd_vel', '/turtle2/cmd_vel')
        ]
    )

    return LaunchDescription([
        turtlesim_node,
        controller_node,
        
        # Add a delay to the spawn command.
        # This gives the turtlesim_node time to start and
        # initialize the /spawn service before we call it.
        TimerAction(
            period=0.5,  # Delay in seconds
            actions=[spawn_turtle2_cmd]
        ),
        
        teleop_turtle2_node
    ])


