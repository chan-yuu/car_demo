# Base image with ROS 2 Humble on Ubuntu 22.04
FROM ros:humble-ros-core-jammy

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install dependencies and tools
RUN apt-get update && apt-get install -y \
    lsb-release \
    wget \
    gnupg2 \
    curl \
    build-essential \
    git \
    vim \
    apt-utils \
    python3-colcon-common-extensions \
    python3-rosdep \
    bash-completion \
    ros-humble-desktop \
    ros-humble-joint-state-publisher \
    ros-humble-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Initialize rosdep
# -------------------------      
RUN rosdep init && rosdep fix-permissions && rosdep update  

# -------------------------
# Install ros_gz from source for Humble + Harmonic compatibility
# -------------------------    
RUN mkdir -p /root/ros_gz_ws/src && \
    cd /root/ros_gz_ws/src && \
    git clone https://github.com/gazebosim/ros_gz.git -b humble && \
    cd /root/ros_gz_ws && \
    apt-get update && \
    rosdep install -r --from-paths src -i -y --rosdistro humble && \
    . /opt/ros/humble/setup.sh && \
    colcon build --symlink-install --parallel-workers=1 --executor sequential \
    && rm -rf /var/lib/apt/lists/*
  
# Source the new workspace automatically
RUN echo "source /root/ros_gz_ws/install/setup.bash" >> ~/.bashrc 

# -------------------------
# Install Gazebo Harmonic
# -------------------------
RUN curl -sSL http://packages.osrfoundation.org/gazebo.gpg | apt-key add - \
    && echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
    > /etc/apt/sources.list.d/gazebo-stable.list \
    && apt-get update && apt-get install -y \
    gz-harmonic \
    gz-tools \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Source ROS 2 automatically
# -------------------------
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc

# Default command: open bash
CMD ["/bin/bash"]
