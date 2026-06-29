FROM ros:humble-ros-core

ARG USERNAME=oper
# Set your graphical environment.
ARG DISPLAY=:0
ARG XDG_RUNTIME_DIR=/run/user/1000
ARG XAUTHORITY="$XDG_RUNTIME_DIR/.mutter-Xwaylandauth*"

RUN apt-get update && apt-get upgrade -y && apt-get install -y sudo
COPY --chmod=755 initcnt /usr/bin
RUN useradd -m -s /bin/bash -G sudo $USERNAME && passwd -d $USERNAME
RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> /home/$USERNAME/.bashrc
RUN echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}
RUN chmod 0440 /etc/sudoers.d/${USERNAME}

RUN echo "#Graphics setup." >> /home/$USERNAME/.bashrc
RUN echo "export DISPLAY=$DISPLAY" >> /home/$USERNAME/.bashrc
RUN echo "export XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR" >> /home/$USERNAME/.bashrc
RUN echo "export XAUTHORITY=$XAUTHORITY" >> /home/$USERNAME/.bashrc

# Ardupilot Build dependencies.
RUN apt-get install -y git python3-colcon-core python3-colcon-bash python3-colcon-cmake \
    python3-colcon-ros python3-colcon-python-setup-py python3-colcon-package-selection \
    python3-colcon-parallel-executor python3-vcstool python3-rosdep
# Micro-XRCE-DDS-Gen dependencies.
RUN apt-get install -y default-jre
# MAVROS dependencies.
RUN apt-get install -y ros-humble-mavros

USER $USERNAME
RUN mkdir -p /home/$USERNAME/fms/src
WORKDIR /home/$USERNAME/fms

# Ardupilot setup.
RUN vcs import --recursive --input \
    https://raw.githubusercontent.com/ArduPilot/ardupilot/master/Tools/ros2/ros2.repos src
RUN AP_DOCKER_BUILD=1 SKIP_AP_EXT_ENV=1 SKIP_AP_GRAPHIC_ENV=0 SKIP_AP_COV_ENV=1 \
    DO_AP_STM_ENV=0 USER=$USERNAME \
    src/ardupilot/Tools/environment_install/install-prereqs-ubuntu.sh -y
RUN sudo rosdep init && rosdep update && rosdep install --from-paths src --ignore-src -r -y

# Micro-XRCE-DDS-Gen setup.
RUN git clone --recurse-submodules --branch v4.7.0 \
    https://github.com/ardupilot/Micro-XRCE-DDS-Gen.git src/Micro-XRCE-DDS-Gen
WORKDIR /home/$USERNAME/fms/src/Micro-XRCE-DDS-Gen
RUN ./gradlew assemble
RUN echo "export PATH=\$PATH:/home/$USERNAME/fms/src/Micro-XRCE-DDS-Gen/scripts" >> \
    ~/.ardupilot_env

# Build Ardupilot.
WORKDIR /home/$USERNAME/fms
# RUN commands are executed as `/bin/sh -c`, which in Ubuntu is /bin/dash. But we need /bin/bash
# to run commands in the ROS environment.
RUN /bin/bash -c "source /opt/ros/$ROS_DISTRO/setup.bash; \
    source ~/.ardupilot_env; \
    colcon build --packages-up-to ardupilot_dds_tests"

# Install Geographic-lib datasets required by MAVROS.
RUN sudo /opt/ros/humble/lib/mavros/install_geographiclib_datasets.sh

# Cleanup.
RUN sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
