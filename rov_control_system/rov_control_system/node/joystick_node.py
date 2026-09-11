import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from rov_control_system.serves.joystick import Joystick


class JoystickNode(Node):
    def __init__(self):
        super().__init__('joystick_node')
        self.joystick = Joystick()
        self.publisher = self.create_publisher(Joy, '/joystick', 10)
        self.timer = self.create_timer(0.01, self.poll_and_publish)

    def poll_and_publish(self):
        msg = Joy()
        msg.header.stamp = self.get_clock().now().to_msg()

        # Populating standard ROS Joy axes: [left_x, left_y, right_x, right_y]
        msg.axes = [
            float(self.joystick.get_place(0)),
            float(self.joystick.get_place(1)),
            float(self.joystick.get_place(2)),
            float(self.joystick.get_place(3))
        ]

        # Populating standard ROS Joy buttons: [a, b, x, y]
        msg.buttons = [
            int(self.joystick.get_button(0)),
            int(self.joystick.get_button(1)),
            int(self.joystick.get_button(2)),
            int(self.joystick.get_button(3))
        ]

        print(f"x: {msg.axes[0]}, y: {msg.axes[1]}")
        self.publisher.publish(msg)

    def apply_deadzone(value: float, threshold: float = 0.05) -> float:
        """Clamps small noise around 0.0 to true zero."""
        if abs(value) < threshold:
            return 0.0
        return value
        
def main(args=None):
    rclpy.init(args=args)
    node = JoystickNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.joystick.cleanup()
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()