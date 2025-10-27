import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleCirclePublisher(Node):
    def __init__(self):
        super().__init__('turtle_circle_publisher')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_cb)  # 10 Hz
        self.v = 1.5   # linear speed
        self.w = 1.0   # angular speed

    def timer_cb(self):
        twist = Twist()
        twist.angular.z = self.w
        twist.linear.x = self.v
        self.pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)

    circle_publisher = TurtleCirclePublisher()

    rclpy.spin(circle_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    circle_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
