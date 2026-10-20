#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


def normalize_angle(angle):
    """Normalize an angle to the range [-pi, pi]."""
    return math.atan2(math.sin(angle), math.cos(angle))


class TurtleDriving(Node):
    def __init__(self):
        super().__init__('turtle_driving')

        self.publisher = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )

        self.pose = None

        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )

        self.get_logger().info('Turtle driving controller started.')

    def pose_callback(self, msg):
        self.pose = msg

    def update_pose(self):
        rclpy.spin_once(self, timeout_sec=0.05)

    def stop(self):
        """Stop the turtle and allow the stop command to be published."""
        msg = Twist()
        for _ in range(3):
            self.publisher.publish(msg)
            self.update_pose()

    def wait_for_pose(self):
        """Wait until turtlesim provides the initial pose."""
        self.get_logger().info('Waiting for turtlesim pose...')
        while rclpy.ok() and self.pose is None:
            self.update_pose()

        return self.pose is not None

    def drive_distance(self, distance, speed=1.0):
        """Drive forward until the requested distance is reached."""
        if self.pose is None:
            return

        start_x = self.pose.x
        start_y = self.pose.y
        msg = Twist()
        msg.linear.x = speed

        while rclpy.ok():
            self.update_pose()

            if self.pose is None:
                continue

            travelled = math.hypot(
                self.pose.x - start_x,
                self.pose.y - start_y
            )

            if travelled >= distance:
                break

            self.publisher.publish(msg)

        self.stop()

    def turn_by(self, angle):
        """Turn by a relative angle using pose feedback."""
        if self.pose is None:
            return

        target = normalize_angle(self.pose.theta + angle)
        msg = Twist()

        while rclpy.ok():
            self.update_pose()

            if self.pose is None:
                continue

            error = normalize_angle(target - self.pose.theta)

            if abs(error) < 0.025:
                break

            msg.linear.x = 0.0
            msg.angular.z = 1.2 if error > 0 else -1.2
            self.publisher.publish(msg)

        self.stop()

    def patrol(self):
        self.get_logger().info('PATROL: moving forward.')
        self.drive_distance(3.0)

        self.get_logger().info('PATROL: turning 180 degrees.')
        self.turn_by(math.pi)

        self.get_logger().info('PATROL: returning toward the start.')
        self.drive_distance(3.0)

        self.stop()
        self.get_logger().info('PATROL complete.')

    def rectangle(self):
        self.get_logger().info('RECTANGLE started.')

        for _ in range(2):
            self.drive_distance(2.0)
            self.turn_by(math.pi / 2)
            self.drive_distance(1.0)
            self.turn_by(math.pi / 2)

        self.stop()
        self.get_logger().info('RECTANGLE complete.')

    def zigzag(self):
        self.get_logger().info('ZIGZAG started.')

        self.drive_distance(1.5)
        self.turn_by(math.pi / 4)

        self.drive_distance(1.5)
        self.turn_by(-math.pi / 2)

        self.drive_distance(1.5)

        self.stop()
        self.get_logger().info('ZIGZAG complete.')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleDriving()

    try:
        if not node.wait_for_pose():
            return

        while rclpy.ok():
            print('\n===== TURTLE DRIVING MENU =====')
            print('P - Patrol')
            print('R - Rectangle')
            print('Z - Zigzag')
            print('Q - Quit')

            try:
                choice = input('Choose P, R, Z, or Q: ').strip().upper()
            except (EOFError, KeyboardInterrupt):
                break

            if choice == 'P':
                node.patrol()
            elif choice == 'R':
                node.rectangle()
            elif choice == 'Z':
                node.zigzag()
            elif choice == 'Q':
                print('Quitting. Stopping the turtle.')
                break
            else:
                print('Invalid choice. Enter P, R, Z, or Q.')

    finally:
        node.stop()
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
