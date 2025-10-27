import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

from enum import Enum

TURTLESIM_ARENA_WIDTH = 11.1

class TurtleLeftRightNode(Node):
    def __init__(self):
        super().__init__('turtle_circle_publisher')
        self.declare_parameter('range', 4.0)
        self.range = self.get_parameter('range').value
        print('TurtleLeftRightNode starting up. range: {}'.format(self.range))

        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(
            Pose,
            'pose',
            self.pose_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.v = 1.5   # linear speed
        self.twist = Twist()
        self.twist.linear.x = self.v
        self.direction = 1 # forward

    def pose_callback(self, pose):
        if pose.x >= TURTLESIM_ARENA_WIDTH/2 + self.range:
            self.direction = -1
        elif pose.x < TURTLESIM_ARENA_WIDTH/2 - self.range:
            self.direction = 1
        self.twist.linear.x = self.v * self.direction
        self.pub.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)

    lr_node = TurtleLeftRightNode()

    rclpy.spin(lr_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    lr_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
