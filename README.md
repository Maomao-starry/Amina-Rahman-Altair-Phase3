# Altair Phase 3 — Amina Rahman

**Student ID:** 240042101
**ROS 2 Distribution:** Jazzy
**Operating System:** Ubuntu 24.04 (WSL)

## Project Overview

This project implements ROS 2 nodes and a turtlesim-based simulation for the Altair Phase 3 coursework. It covers telemetry communication, keyboard-style turtle driving, investigation of competing velocity publishers, and autonomous waypoint navigation with obstacle handling.

## Requirements

* Ubuntu 24.04
* ROS 2 Jazzy
* Python 3
* `colcon`
* `turtlesim`

## Build the Package

Open a terminal and run:

```bash
source /opt/ros/jazzy/setup.bash
cd ~/altair_phase3_ws
colcon build --symlink-install --packages-select altair_phase3
source install/setup.bash
```

## Task 1 — Mars Telemetry Publisher and Monitor

Task 1 implements ROS 2 publisher and subscriber nodes for Mars rover telemetry.

### Main Features

* The telemetry publisher publishes rover telemetry messages.
* The monitor subscribes to the telemetry topic and receives the messages.
* ROS 2 topics allow the two nodes to communicate asynchronously.

### Run

Open a terminal:

```bash
source /opt/ros/jazzy/setup.bash
source ~/altair_phase3_ws/install/setup.bash
ros2 run altair_phase3 telemetry_pub
```

Open another terminal:

```bash
source /opt/ros/jazzy/setup.bash
source ~/altair_phase3_ws/install/setup.bash
ros2 run altair_phase3 telemetry_monitor
```

To inspect the telemetry topic:

```bash
ros2 topic info /mars_telemetry
ros2 topic echo /mars_telemetry
```

## Task 2A — Turtle Driving Menu

Task 2A implements a menu-driven interface for controlling the turtlesim turtle.

### Main Features

* Provides movement commands through a simple menu.
* Sends velocity commands to the turtle using ROS 2.
* Supports the implemented movement options, including pause/stop and quitting the menu.
* Uses the `/turtle1/cmd_vel` topic to control turtle movement.

### Run

First, start the turtlesim simulator:

```bash
ros2 run turtlesim turtlesim_node
```

In another terminal, run the driving menu:

```bash
source /opt/ros/jazzy/setup.bash
source ~/altair_phase3_ws/install/setup.bash
ros2 run altair_phase3 turtle_driving
```

If the executable name differs in the installed package, check the available executables with:

```bash
ros2 pkg executables altair_phase3
```

## Task 2B — Investigating Competing Velocity Publishers

Task 2B investigates what happens when multiple ROS 2 publishers send velocity commands to the same turtle command topic.

### Main Features

* Uses ROS 2 publishers to send velocity messages.
* Examines communication through `/turtle1/cmd_vel`.
* Demonstrates that competing publishers can issue conflicting movement commands.
* Uses topic and node inspection commands to investigate the active publishers.

### Useful Commands

```bash
ros2 topic info /turtle1/cmd_vel --verbose
ros2 node list
ros2 topic echo /turtle1/cmd_vel
```

The publisher information can be used to identify which nodes are publishing velocity commands to the turtle.

## Task 3 — Waypoint Mission and Obstacle Handling

Task 3 implements an autonomous waypoint mission using ROS 2 and turtlesim.

### Waypoint Sequence

The turtle visits the following locations in order:

1. **Bottle:** `(8.0, 5.5)`
2. **Mallet:** `(8.0, 8.0)`
3. **Base:** `(5.5, 5.5)`

The mission controller reads the turtle's pose and publishes velocity commands to guide it toward each waypoint.

### Main Features

* Subscribes to `/turtle1/pose` to obtain the turtle's current position.
* Publishes movement commands to `/turtle1/cmd_vel`.
* Visits the Bottle, Mallet, and Base waypoints in sequence.
* Detects obstacle-state messages received on `/field_blocked`.
* Stops and pauses the mission when an obstacle is detected.
* Does not automatically resume when the obstacle clears.
* Provides the `/resume_mission` service to resume the mission after the obstacle is cleared.
* Rejects a resume request while an obstacle is still present.
* Reports waypoint arrivals and mission completion through ROS 2 logging.

### Build and Run

Build the package:

```bash
source /opt/ros/jazzy/setup.bash
cd ~/altair_phase3_ws
colcon build --symlink-install --packages-select altair_phase3
source install/setup.bash
```

Launch the simulator and waypoint mission together:

```bash
ros2 launch altair_phase3 waypoint_mission.launch.py
```

### Test Obstacle Handling

Open a second terminal and source the ROS 2 environment:

```bash
source /opt/ros/jazzy/setup.bash
source ~/altair_phase3_ws/install/setup.bash
```

Simulate obstacle detection:

```bash
ros2 topic pub --once /field_blocked std_msgs/msg/Bool "{data: true}"
```

Try to resume while the obstacle is present. The request should be rejected:

```bash
ros2 service call /resume_mission std_srvs/srv/Trigger "{}"
```

Clear the obstacle:

```bash
ros2 topic pub --once /field_blocked std_msgs/msg/Bool "{data: false}"
```

The mission remains paused until the resume service is called:

```bash
ros2 service call /resume_mission std_srvs/srv/Trigger "{}"
```

### Verify the ROS 2 Interfaces

```bash
ros2 topic info /turtle1/cmd_vel --verbose
ros2 topic info /turtle1/pose
ros2 topic info /field_blocked
ros2 service type /resume_mission
```

### Expected Mission Output

During a successful run, the console reports waypoint arrivals and ends with a message similar to:

```text
ARRIVED: Bottle
NEXT WAYPOINT: Mallet
ARRIVED: Mallet
NEXT WAYPOINT: Base
ARRIVED: Base
DONE: Bottle, Mallet, and Base completed.
```

When an obstacle is detected, the mission pauses and requires an explicit resume request after the obstacle clears.

## Project Structure

```text
altair_phase3/
├── altair_phase3/
│   ├── __init__.py
│   ├── telemetry_pub.py (entry point: telemetry_pub)
│   ├── mission_control_monitor.py (entry point: telemetry_monitor)
│   ├── turtle_driving.py
│   └── waypoint_mission.py
├── launch/
│   └── waypoint_mission.launch.py
├── resource/
├── package.xml
├── setup.cfg
├── setup.py
└── README.md
```

The filenames listed above describe the intended project layout. Check the actual package directory if an executable or file has a different name.

## Evidence and Testing

Demonstration videos and notes are maintained separately from the ROS 2 source code.

The tests performed include:

* Telemetry publisher/subscriber communication.
* Menu-driven turtle movement.
* Investigation of multiple velocity publishers.
* Sequential waypoint navigation.
* Obstacle-triggered stopping and pausing.
* Rejection of resume requests while blocked.
* Explicit resumption after the obstacle clears.

## Author

**Amina Rahman**
**Student ID:** 240042101
