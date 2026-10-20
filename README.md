# Altair Phase 3

**Student:** Amina Rahman  
**Student ID:** 240042101

This repository contains my ROS 2 implementations for Project Altair Phase 3.

## Task 1: Mars Rover Telemetry

Task 1 implements a telemetry publisher and mission-control monitor.

### Nodes

- `mars_telemetry_publisher`
  - Publishes telemetry every second.
  - Simulates battery depletion and increasing internal temperature.
  - Publishes battery percentage, temperature, wheel speed, and elapsed mission time.

- `mission_control_monitor`
  - Subscribes to the telemetry topic.
  - Displays the received measurements.
  - Issues a warning when the battery drops below 25%.

### Topic and message type

- Topic: `/mars_telemetry`
- Message type: `std_msgs/msg/String`
- Data format: JSON encoded inside the String message.

JSON inside a String message keeps this example simple without requiring a custom message definition.

### Requirements

- ROS 2 Jazzy
- Python 3
- `rclpy`
- `std_msgs`

### Build

From the workspace root:

    source /opt/ros/jazzy/setup.bash
    colcon build --symlink-install --packages-select altair_phase3
    source install/setup.bash

### Run the publisher

In the first terminal:

    source /opt/ros/jazzy/setup.bash
    source ~/altair_phase3_ws/install/setup.bash
    ros2 run altair_phase3 telemetry_pub

### Run the monitor

In a second terminal:

    source /opt/ros/jazzy/setup.bash
    source ~/altair_phase3_ws/install/setup.bash
    ros2 run altair_phase3 telemetry_monitor

### Inspect the topic

    ros2 topic info /mars_telemetry
    ros2 topic echo /mars_telemetry

The monitor displays a low-battery warning when the battery percentage falls below 25%.

## Project status

Task 1's publisher and monitor have been implemented and tested. Other Phase 3 tasks will be added as they are completed.
