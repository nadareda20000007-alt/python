import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

from multi_sensor_validator.ultrasonic_sensor import Ultrasonic

class UltrasonicNode(Node):

    def __init__(self):
        super().__init__('ultrasonic_node')
        self.publisher_ = self.create_publisher(Int32, '/ultrasonic_range', 10)
        self.sensor = Ultrasonic()
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = Int32()
        msg.data = self.sensor.read()
        self.publisher_.publish(msg)
        self.get_logger().info(f'Ultrasonic: {msg.data} cm')


def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()