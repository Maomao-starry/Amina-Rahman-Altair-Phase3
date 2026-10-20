import json
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MarsTelemetryPublisher(Node):

    def __init__(self):
        super().__init__('mars_telemetry_publisher')

        self.publisher_ = self.create_publisher(
            String,
            '/mars_telemetry',
            10
        )

        self.start_time = time.monotonic()
        self.battery = 100.0
        self.temperature = 25.0

        self.timer = self.create_timer(1.0, self.publish_telemetry)

        self.get_logger().info('Mars telemetry publisher started.')

    def publish_telemetry(self):
        elapsed_time = time.monotonic() - self.start_time

        # Simulate the rover's battery slowly decreasing.
        self.battery = max(0.0, 100.0 - elapsed_time * 2.0)

        # Simulate the rover warming up during its mission.
        self.temperature = min(65.0, 25.0 + elapsed_time * 0.5)

        telemetry = {
            'battery_percent': round(self.battery, 1),
            'temperature_celsius': round(self.temperature, 1),
            'wheel_speed_mps': 0.5,
            'mission_time_seconds': round(elapsed_time, 1)
        }

        message = String()
        message.data = json.dumps(telemetry)
        self.publisher_.publish(message)

        self.get_logger().info(
            f"Published telemetry: {message.data}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = MarsTelemetryPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
