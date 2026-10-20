import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MissionControlMonitor(Node):

    def __init__(self):
        super().__init__('mission_control_monitor')

        self.subscription = self.create_subscription(
            String,
            '/mars_telemetry',
            self.telemetry_callback,
            10
        )

        self.get_logger().info('Mission control monitor started.')

    def telemetry_callback(self, message):
        try:
            data = json.loads(message.data)

            battery = float(data['battery_percent'])
            temperature = float(data['temperature_celsius'])
            wheel_speed = float(data['wheel_speed_mps'])
            mission_time = float(data['mission_time_seconds'])

            self.get_logger().info(
                f"Mission time: {mission_time:.1f} s | "
                f"Battery: {battery:.1f}% | "
                f"Temperature: {temperature:.1f} °C | "
                f"Wheel speed: {wheel_speed:.2f} m/s"
            )

            if battery < 25.0:
                self.get_logger().warning(
                    f"LOW BATTERY WARNING: {battery:.1f}% remaining!"
                )

        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            self.get_logger().error(
                'Received invalid telemetry data.'
            )


def main(args=None):
    rclpy.init(args=args)
    node = MissionControlMonitor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
