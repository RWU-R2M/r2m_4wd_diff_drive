FROM ros:jazzy

ARG ROS_DISTRO=jazzy
ARG ROS_WS=/root/ros2_ws

ENV ROS_DISTRO=${ROS_DISTRO}
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
    ros-${ROS_DISTRO}-xacro \
    ros-${ROS_DISTRO}-ros2-control \
    ros-${ROS_DISTRO}-controller-manager \
    ros-${ROS_DISTRO}-control-msgs \
    ros-${ROS_DISTRO}-realtime-tools \
    ros-${ROS_DISTRO}-hardware-interface \
    ros-${ROS_DISTRO}-hardware-interface-testing \
    ros-${ROS_DISTRO}-ament-cmake \
    python3-colcon-common-extensions \
    qtbase5-dev \
    qt5-qmake \
    qtbase5-dev-tools \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p ${ROS_WS}/src

# Copy the source files
COPY ./ros2_control_demos ${ROS_WS}/src/ros2_control_demos
COPY ./submodules/ros_odrive ${ROS_WS}/src/ros_odrive

# Change to workspace directory before running rosdep
WORKDIR ${ROS_WS}

# Initialize rosdep and install dependencies
RUN apt-get update && \
    rosdep update && \
    rosdep install -y --ignore-src --from-paths src || true

# Build the workspace
RUN . /opt/ros/${ROS_DISTRO}/setup.sh \
    && colcon build --symlink-install

# Source the environment in .bashrc
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc && \
    echo "source ${ROS_WS}/install/setup.bash" >> /root/.bashrc

CMD ["bash"]