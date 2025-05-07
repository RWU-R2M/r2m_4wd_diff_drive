#!/bin/bash
# ...save as start_hardware_stack.sh...

# Set your CAN interface name here, or pass as argument
CAN_IFACE="${CAN_IFACE:-can0}"

# Check CAN interface variable
if [ -z "$CAN_IFACE" ]; then
  echo "Error: CAN_IFACE environment variable not set."
  exit 1
fi

# Bring up CAN interface at 500000 baud
echo "Bringing up $CAN_IFACE at 500000 baud..."
sudo ip link set $CAN_IFACE down 2>/dev/null
sudo ip link set $CAN_IFACE type can bitrate 500000
sudo ip link set $CAN_IFACE up

if [ $? -ne 0 ]; then
  echo "Error: Failed to bring up $CAN_IFACE"
  exit 1
fi

# Wait a couple seconds
sleep 2

# Set ROS_DOMAIN_ID (change as needed)
export ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-0}
echo "ROS_DOMAIN_ID set to $ROS_DOMAIN_ID"

# Launch first container
echo "Launching first container..."
docker compose -f docker/docker-compose-hardware.yml up 

if [ $? -ne 0 ]; then
  echo "Error: Failed to launch first container."
  exit 1
fi

# Wait for the first container to be running
echo "Waiting for first container to be running..."
for i in {1..10}; do
  status=$(docker inspect -f '{{.State.Running}}' r2m_4wd_diff_drive_odrive 2>/dev/null)
  if [ "$status" == "true" ]; then
    echo "First container is running."
    break
  fi
  sleep 1
done

if [ "$status" != "true" ]; then
  echo "Error: First container did not start."
  exit 1
fi

# Launch second container (example, replace with your actual service name)
SECOND_CONTAINER=my_second_container
echo "Launching second container..."
docker compose -f docker/docker-compose-hardware.yml up -d $SECOND_CONTAINER

if [ $? -ne 0 ]; then
  echo "Error: Failed to launch second container."
  exit 1
fi

# Wait for confirmation (container running)
echo "Waiting for second container to be running..."
for i in {1..10}; do
  status2=$(docker inspect -f '{{.State.Running}}' $SECOND_CONTAINER 2>/dev/null)
  if [ "$status2" == "true" ]; then
    echo "Second container is running."
    break
  fi
  sleep 1
done

if [ "$status2" != "true" ]; then
  echo "Error: Second container did not start."
  exit 1
fi

echo "Both containers are running. Finished."
