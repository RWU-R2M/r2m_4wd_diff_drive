# R2M 4WD Differential Drive Robot

## Build Status

| Build Step | Status |
|------------|--------|
| Overall Build | [![Multi-Architecture Docker Build](https://github.com/rwu-r2m/r2m_diff_bot/actions/workflows/docker-push.yml/badge.svg)](https://github.com/rwu-r2m/r2m_diff_bot/actions/workflows/docker-push.yml) |
| AMD64 Build | [![AMD64 Build Status](https://github.com/rwu-r2m/r2m_diff_bot/actions/workflows/docker-push.yml/badge.svg?job=build-push-amd64)](https://github.com/rwu-r2m/r2m_diff_bot/actions/workflows/docker-push.yml) |
| ARM64 Build | [![ARM64 Build Status](https://github.com/rwu-r2m/r2m_diff_bot/actions/workflows/docker-push.yml/badge.svg?job=build-push-arm64)](https://github.com/rwu-r2m/r2m_diff_bot/actions/workflows/docker-push.yml) |
| Multi-Arch Manifest | [![Multi-Arch Manifest](https://github.com/rwu-r2m/r2m_diff_bot/actions/workflows/docker-push.yml/badge.svg?job=create-manifests)](https://github.com/rwu-r2m/r2m_diff_bot/actions/workflows/docker-push.yml) |

## Project Overview

This repository implements a 4-wheel drive (4WD) differential drive robot based on the ROS2 Control framework. It extends the standard diffbot example from ros2_control_demos to support a 4WD configuration with ODrive motor controllers via CAN bus.

System components:
- Four-wheel drive with differential steering mechanism
- ODrive motor controllers with CAN communication protocol
- Docker containers for cross-architecture deployment
- ROS2 Control hardware interface implementation

## Setup Instructions

```bash
git clone git@github.com:rwu-r2m/r2m_4wd_diff_drive.git && cd r2m_4wd_diff_drive
```

```bash
git submodule update --init
```

```bash
docker compose -f docker/build.yml build
```

## Docker Compose Files

Docker configuration files:

- `docker/build.yml`: Docker image build configuration
- `docker/docker-compose.yml`: Simulation environment with mock hardware interfaces
- `docker/docker-compose-hardware.yml`: Hardware integration with physical motors
- `docker/docker-compose-amd64.yml`: AMD64 architecture configuration
- `docker/docker-compose-arm64.yml`: ARM64 architecture configuration

## Start without real hardware:

Execute with simulated hardware interface:

```bash
# Grant X server access to the container (required for GUI applications)
xhost local:user
```

```bash
docker compose -f docker/docker-compose.yml up
```

If the simulation GUI fails to start, check that X server permissions are properly set. The `xhost local:user` command allows the Docker container to access your local X server for displaying GUI applications.

## Start with real hardware:

Connect to physical hardware components via CAN interface.

### Hardware Setup
1. **CAN interface connection**: Connect the CAN2USB adapter to the diff-base
2. **CAN interface configuration**: Set up the Linux CAN interface
   ```bash
   sudo ip link set can0 up type can bitrate 250000
   ```
   If interface doesn't exist:
   ```bash
   sudo ip link add dev can0 type can bitrate 250000
   sudo ip link set can0 up
   ```

3. **Power system initialization**: 
   - Connect power supply (bike cell)
   - Enable main power switch
   - Verify ODrive controller status LEDs

4. **Launch hardware container**:
   ```bash
   docker compose -f docker/docker-compose-hardware.yml up
   ```

### Command Interface

To send velocity commands:

```bash
ros2 topic pub --rate 30 /cmd_vel geometry_msgs/msg/TwistStamped "
       twist:
         linear:
           x: 0.2
           y: 0.0
           z: 0.0
         angular:
           x: 0.0
           y: 0.0
           z: 0.3"
```

Single command format:

```bash
ros2 topic pub -1 /cmd_vel geometry_msgs/msg/TwistStamped "{header: {stamp: {sec: 0}, frame_id: 'base_link'}, twist: {linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.3}}}"
```

## Modifications from Standard Diffbot

Implemented extensions to the original diffbot implementation:

1. **4WD configuration**: 
   - Independent control of 4 wheel motors
   - Modified controller parameters for multi-wheel configuration per side

2. **ODrive integration**: 
   - CAN bus communication interface
   - odrive_ros2_control hardware_interface plugin implementation

3. **Docker implementation**:
   - Multi-architecture compatibility (AMD64/ARM64)
   - Separate runtime environments for simulation and hardware testing

4. **Parameter modifications**:
   - Wheel geometry parameters for 4WD system
   - ODrive-specific CAN bus parameters

## Hardware Interface Variants

### Mock Hardware Interface
- Simulated motor/encoder feedback
- Command reception without physical hardware
- Used for algorithm testing and development
- No hardware dependencies

### Physical Hardware Interface
- ODrive motor controller communication via CAN
- Real-time sensor data acquisition
- Physical motor command transmission
- Full hardware dependencies

## Troubleshooting

### Odometry Data Missing

**Symptom**: No odometry data or abnormal motor behavior

**Cause**: Incorrect ODrive CAN ID configuration

**Solution**: 
- Verify ODrive CAN IDs (ID 0 for left motors, ID 1 for right motors)
- Use ODrive Tool to check/modify CAN configuration

### Directional Control Issues

**Symptom**: Wheels rotating in same direction during turn commands

**Solution**: 
1. Check controller configuration (bringup/config/)
2. Rebuild and restart after parameter modification

### Command Execution Failure

**Symptom**: No response to velocity commands

**Causes**:
1. **Topic mismatch**: Verify publishing to `/cmd_vel` with correct message type
2. **Controller state**: Verify controller status:
   ```bash
   ros2 control list_controllers
   ```
3. **Hardware communication**: Check ODrive status and CAN communication

### CAN Communication Issues

**Symptom**: Hardware interface errors or timeout

**Diagnostics**:
- Check interface status:
  ```bash
  ip -details link show can0
  ```
- Monitor CAN traffic:
  ```bash
  candump can0
  ```
- Reset interface if necessary:
  ```bash
  sudo ip link set can0 down
  sudo ip link set can0 up type can bitrate 250000
  ```

## References
- [ROS2 Control Demos](https://github.com/ros-controls/ros2_control_demos)
- [ODrive ROS2 Package](https://github.com/odriverobotics/ros_odrive)
- [ros2_control Documentation](https://control.ros.org/master/index.html)
- [Differential Drive Controller Documentation](https://control.ros.org/master/doc/controllers/diff_drive/userdoc.html)