FROM fbe-dockerreg.rwu.de/prj-iki-ros2/orga/ros2-docker-base:jazzy

ARG ROS_DISTRO=jazzy
ARG ROS_WS=/root/ros2_ws

ENV ROS_DISTRO=${ROS_DISTRO}

RUN apt-get update \
    && apt install -y \
    ros-${ROS_DISTRO}-xacro \
    ros-${ROS_DISTRO}-ros2-control \
    && rm -rf /var/lib/apt/lists/*


COPY ./ros2_control_demos ${ROS_WS}/src/ros2_control_demos
COPY submodules/ros_odrive ${ROS_WS}/src/ros_odrive

RUN apt-get update && rosdep install -y --ignore-src --from-paths src

RUN cd ${ROS_WS}/ \
  && . /opt/ros/${ROS_DISTRO}/setup.sh \
  && colcon build --symlink-install