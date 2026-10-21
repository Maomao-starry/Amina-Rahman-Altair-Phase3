import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Bool
from std_srvs.srv import Trigger


class WaypointMission(Node):
    def __init__(self):
        super().__init__('waypoint_mission')

        self.cmd_pub = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )
        self.blocked_sub = self.create_subscription(
            Bool, '/field_blocked', self.blocked_callback, 10
        )
        self.resume_service = self.create_service(
            Trigger, '/resume_mission', self.resume_callback
        )

        # Required mission order and target coordinates.
        self.waypoints = [
            ('Bottle', 8.0, 5.5),
            ('Mallet', 8.0, 8.0),
            ('Base', 5.5, 5.5),
        ]

        self.pose = None
        self.index = 0
        self.blocked = False
        self.paused = False
        self.completed = False

        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Waypoint mission started.')
        self.get_logger().info(
            'Waiting for turtle pose before moving.'
        )

    def pose_callback(self, msg):
        self.pose = msg

    def publish_stop(self):
        self.cmd_pub.publish(Twist())

    def blocked_callback(self, msg):
        if msg.data:
            if not self.blocked:
                self.blocked = True

                if not self.completed:
                    self.paused = True
                    self.publish_stop()
                    self.get_logger().warning(
                        'OBSTACLE DETECTED: mission paused.'
                    )
                else:
                    self.get_logger().warning(
                        'Obstacle reported after mission completion.'
                    )
        else:
            if self.blocked:
                self.blocked = False
                self.get_logger().info(
                    'Obstacle cleared. Call /resume_mission to continue.'
                )

    def resume_callback(self, request, response):
        if self.blocked:
            response.success = False
            response.message = (
                'Resume rejected: obstacle is still present.'
            )
        elif self.pose is None:
            response.success = False
            response.message = (
                'Resume rejected: waiting for turtle pose.'
            )
        elif self.completed:
            response.success = False
            response.message = (
                'Resume rejected: mission is already complete.'
            )
        elif not self.paused:
            response.success = False
            response.message = (
                'Resume rejected: mission is not paused.'
            )
        else:
            self.paused = False
            response.success = True
            response.message = 'Mission resumed.'
            self.get_logger().info(
                'Mission resumed by service request.'
            )

        return response

    def control_loop(self):
        if self.completed or self.blocked or self.paused:
            self.publish_stop()
            return

        if self.pose is None:
            self.publish_stop()
            return

        if self.index >= len(self.waypoints):
            self.completed = True
            self.publish_stop()
            self.get_logger().info(
                'DONE: Bottle, Mallet, and Base completed.'
            )
            return

        name, target_x, target_y = self.waypoints[self.index]

        dx = target_x - self.pose.x
        dy = target_y - self.pose.y
        distance = math.hypot(dx, dy)

        if distance < 0.15:
            self.publish_stop()
            self.get_logger().info(f'ARRIVED: {name}')
            self.index += 1

            if self.index >= len(self.waypoints):
                self.completed = True
                self.get_logger().info(
                    'DONE: Bottle, Mallet, and Base completed.'
                )
            else:
                next_name, _, _ = self.waypoints[self.index]
                self.get_logger().info(
                    f'NEXT WAYPOINT: {next_name}'
                )
            return

        desired_heading = math.atan2(dy, dx)
        heading_error = math.atan2(
            math.sin(desired_heading - self.pose.theta),
            math.cos(desired_heading - self.pose.theta)
        )

        command = Twist()

        if abs(heading_error) > 0.30:
            command.angular.z = max(
                -1.5, min(1.5, 3.0 * heading_error)
            )
        else:
            command.linear.x = min(1.5, distance)
            command.angular.z = max(
                -1.5, min(1.5, 3.0 * heading_error)
            )

        self.cmd_pub.publish(command)

    def destroy_node(self):
        try:
            if rclpy.ok():
                self.publish_stop()
        except Exception as exc:
            self.get_logger().debug(
                f'Could not publish final stop during shutdown: {exc}'
            )
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = WaypointMission()

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
