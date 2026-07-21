AIRSHIP Awareness, Anticipation and Adaptation System
=====================================================
This is the WIP Awareness, Anticipation and Adaptation System (A3Sys) used for [AIRSHIP project][1]. Where we test the usage of the [SysSelf metacontroller][2] for the autonomous operation of the Wing-In-Ground drone.

Installation
------------
The environment used to develop, build and test the system is a container running Ubuntu 22 with ROS 2. The container tool used here is [Podman][3]. Although all container related sources are OCI compliant, so Docker should also work.

The image used will be based on ROS2 Humble taken from the [OSRF Docker images][4]. Building [Ardupilot][5] for our use case.
```sh
cd <project_directory>
podman build -t fms:latest .
```

We will create an privileged, [rootless container][6]. For the moment, we will run a simple init program (`initcnt`) to keep the container available in the background and configure the system to use the host graphics.
```sh
podman run -d --privileged --userns=keep-id -v $XDG_RUNTIME_DIR:$XDG_RUNTIME_DIR -v /dev/dri:/dev/dri:rslave -v /tmp:/run/host/tmp:slave -v ./ros_pkg:/home/oper/fms/src/a3sys:Z --hostname=fms --name fms localhost/fms:latest initcnt
podman ps  # Check that the created container is running.
```
Note that to [enable the host-container volume to work with a host OS having SELinux labels for the directories][7] (such as Fedora) we have to append a `:Z` to the volume path.

You can then enter the container with the following command.
```sh
podman exec -it -u root fms_dev login oper  # Login as user "oper".
```
We enter through `login` to initialize the environment as usual, that is, sourcing `~/.profile`, `~/.bashrc` etc. Still, all configuration is intended to place all the setup required in the `~/.bashrc` with the intention of allowing a simpler entrypoint.

As this is currently a development environment, we are mounting the a3sys project directory as a volume inside the container. Requiring us to manually build it.
```sh
oper@fms $ cd fms
oper@fms $ colcon build --packages-up-to a3sys
oper@fms $ source install/local_setup.bash
oper@fms $ mkdir sims
oper@fms $ cd sims
oper@fms $ ros2 launch a3sys mission_launch.py
```
You should then see the logs of the simulation starting, the ardupilot initializing and the mission manager providing waypoints and commanding the drone to takeoff. All the logs are stored in the default directory `~/.ros/log/`. Also a map with the aircraft taking off should appear.

MissionPlanner
--------------
If you want to connect to the simulated drone with the Ground Control Station software Mission Planner you need to select in the top right corner UDP connection to `127.0.0.1:14550`.

Troubleshooting
---------------
Should you have a problem running a GUI inside the container with "Authorization required, but no authorization protocol specified" error, then you should extend the X permission in the host with the following command.
```sh
 $ xhost +local:$HOSTNAME
```

[1]: https://airshipproject.eu
[2]: https://github.com/aslab/sys_self_mc
[3]: https://docs.podman.io/en/latest/
[4]: https://github.com/osrf/docker_images
[5]: https://github.com/ArduPilot/ardupilot/
[6]: https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md
[7]: https://libraibex.com/posts/podman-volumes-permission-denied/
