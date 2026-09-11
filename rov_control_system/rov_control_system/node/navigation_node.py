import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Int16MultiArray
from rov_control_system.serves.navigation import NavigationServiceImpl


class NavigationNode(Node):
    def __init__(self):
        super().__init__('navigation_node')

        # Configuration
        self.thruster_ids = ["T1", "T2", "T3", "T4"]
        
        # Navigation Service with smoothing strategy
        self.service = NavigationServiceImpl(
            self.thruster_ids, 
            smoothing_strategy="exponential", 
            alpha=0.2
        )

        # Safety Watchdog Setup
        self.last_joystick_time = None  # None until first joystick message is received
        self.joystick_timeout_sec = 0.5  # Timeout threshold in seconds

        # ROS 2 Interfaces
        self.subscription = self.create_subscription(
            Joy,
            '/joystick',
            self._on_joystick_data,
            10
        )
        self.publisher = self.create_publisher(Int16MultiArray, '/thruster_pwm', 10)

        # Control loop running at 20 Hz (0.05s)
        self.timer = self.create_timer(0.05, self._timer_callback)
        self.get_logger().info("Navigation Node initialized and running at 20 Hz.")

    def _on_joystick_data(self, msg: Joy):
        """Callback triggered when raw joystick data arrives on /joystick."""
        # Refresh watchdog timestamp
        self.last_joystick_time = self.get_clock().now()
        # Delegate input mapping & deadzone processing to service layer
        self.service.update_target(msg.axes)

    def _timer_callback(self):
        """Timer callback: checks failsafes, steps smoother forward, and publishes PWMs."""
        # Safety Check: Watchdog timeout (only runs after first joystick msg received)
        if self.last_joystick_time is not None:
            elapsed_time = (self.get_clock().now() - self.last_joystick_time).nanoseconds / 1e9
            if elapsed_time > self.joystick_timeout_sec:
                self.get_logger().warn(
                    f"Joystick timeout! Signal lost for {elapsed_time:.1f}s. Resetting targets to neutral (1500).",
                    throttle_duration_sec=2.0
                )
                # Reset target axes to 0.0 (Neutral PWM)
                self.service.update_target([0.0, 0.0])

        # 1. Advance current PWM values toward target via active smoother
        smoothed_pwms = self.service.smooth_step()

        # 2. Extract values and convert to integers for Int16MultiArray
        current_pwms = [int(smoothed_pwms[tid]) for tid in self.thruster_ids]

        pwm_msg = Int16MultiArray()
        pwm_msg.data = current_pwms

        self.publisher.publish(pwm_msg)
        
        # 3. Log active strategy and published PWM outputs
        strategy = self.service.current_strategy
        self.get_logger().info(f"[{strategy.upper()} SMOOTHING] Published PWM: {pwm_msg.data}")

    def emergency_stop(self):
            """Forces all thruster outputs directly to neutral (1500 us) immediately."""
            if rclpy.ok():
                self.get_logger().warn("Emergency stop triggered. Neutralizing all thrusters.")
                pwm_msg = Int16MultiArray()
                pwm_msg.data = [1500] * len(self.thruster_ids)
                self.publisher.publish(pwm_msg)

def main(args=None):
    rclpy.init(args=args)
    node = NavigationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Trigger emergency stop before destroying the node context
        node.emergency_stop()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()