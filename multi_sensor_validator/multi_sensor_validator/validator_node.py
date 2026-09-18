import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String

from multi_sensor_validator.validator import Validator


class ValidatorNode(Node):

    def __init__(self):
        super().__init__('validator_node')
        self.validator = Validator(tolerance_cm=20)

        self.latest_ultrasonic = None
        self.latest_infrared = None

        self.publisher_ = self.create_publisher(String, '/validation_result', 10)

        self.ultrasonic_sub = self.create_subscription(
            Int32, '/ultrasonic_range', self.ultrasonic_callback, 10)
        self.infrared_sub = self.create_subscription(
            Int32, '/infrared_range', self.infrared_callback, 10)

    def ultrasonic_callback(self, msg: Int32):
        self.latest_ultrasonic = msg.data
        self.try_validate()

    def infrared_callback(self, msg: Int32):
        self.latest_infrared = msg.data
        self.try_validate()

    def try_validate(self):
        if self.latest_ultrasonic is None or self.latest_infrared is None:
            return

        result = self.validator.compare(self.latest_ultrasonic, self.latest_infrared)

        msg = String()
        msg.data = (
            f'Ultrasonic: {self.latest_ultrasonic} cm, '
            f'Infrared: {self.latest_infrared} cm -> {result}'
        )
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ValidatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()