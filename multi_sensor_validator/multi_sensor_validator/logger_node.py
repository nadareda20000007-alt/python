import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from  multi_sensor_validator.logger import Logger


class LoggerNode(Node):

    def __init__(self):
        super().__init__('logger_node')
        self.logger_util = Logger()
        self.subscription = self.create_subscription(
            String, '/validation_result', self.listener_callback, 10)

    def listener_callback(self, msg: String):
        self.logger_util.log(msg.data)


def main(args=None):
    rclpy.init(args=args)
    node = LoggerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()