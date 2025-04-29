# iki_diff_base 
Current setup is just the stripped demo-example from ros2 controll for the diff-controler.

## Setup Instructions

```bash
git clone git@gitlab.rwu.de:prj-iki-ros2/robots/iki_diff_base.git && cd iki_diff_base
```

```bash
git submodule update --init
```

```bash
docker compose -f docker/build.yml build
```

## Start without real hardware:

```bash
docker compose -f docker/docker-compose.yml up
```

## Start with real hardware:

### Hardware
1. `Connect` your laptop via the can2usb adapter to the diff-base
2. `Power up` the diff-base (bike cell)

From now on u have to be connected via the usb2can adapter
```bash
sudo ip link set can0 up type can bitrate 250000
```
```bash
docker compose -f docker/docker-compose-hardware.yml up
```

### Sending a simple movement command
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

## Debugging

In case there is no odometry for a given link, or both motors are turing in the same direction no matter what, check if the odrives are configured with CAN ID 0 and 1.

## Important links
https://github.com/ros-controls/ros2_control_demos

https://articulatedrobotics.xyz/tutorials/mobile-robot/applications/ros2_control-real/