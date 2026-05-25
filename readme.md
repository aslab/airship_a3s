AIRSHIP Awareness, Anticipation and Adaptation System
=====================================================
This is the WIP Awareness, Anticipation and Adaptation System (A3S) used for [AIRSHIP project][1]. Where we test the usage of the [SysSelf metacontroller][2] for the autonomous operation of the Wing-In-Ground drone.

Installation
------------
The environment used to develop, build and test the system is a container running Ubuntu 22 with ROS 2. The container tool used here is [Podman][3]. Although all container related sources are OCI compliant, so Docker should also work.

The image used will be based on ROS2 Humble taken from the [OSRF Docker images][4]. Building [Ardupilot][5] for our use case.
```sh
cd <project_directory>
podman build --cpuset-cpus=0-7 -t fms:latest .
```
The `--cpuset-cpus=0-7` is an optional argument to specify which CPUS speficially are allowed to to be used by the building process. This helps preventing resource starvation in intensive tasks such as the Ardupilot compilation.

We will create an unprivileged, [rootless container][6]. For the moment, we will run a simple init program (`initcnt`) to keep the container available in the background.
```sh
podman run -d --userns=keep-id --cpuset-cpus=2-12 -v ./ros_pkg:/home/oper/fms/src/a3s:Z --hostname=fms --name fms_dev localhost/fms:latest initcnt
podman ps  # Check that the created container is running.
```
Note that to [enable the host-container volume to work with a host OS having SELinux labels for the directories][7] (such as Fedora) we have to append a `:Z` to the volume path.

You can then enter the container with the following command.
```sh
podman exec -it -u root fms login oper  # Login as user "oper".
```
We enter through `login` to initialize the environment as usual, that is, sourcing `~/.profile`, `~/.bashrc` etc. Still, all configuration is intended to place all the setup required in the `~/.bashrc` with the intention of allowing a simpler entrypoint.

As this is currently a development environment, we are mounting the a3s project directory as a volume inside the container. Which means that now is the time the build it.
```sh
oper@fms $ cd fms
oper@fms $ colcon build --packages-up-to a3s
oper@fms $ source install/local_setup.bash
oper@fms $ mkdir sims
oper@fms $ cd sims
oper@fms $ ros2 launch a3s mission_launch.py
```
You should then see the logs of the simulation starting, the ardupilot initializing and the mission manager providing waypoints and commanding the drone to takeoff. All the logs are stored in the default directory `~/.ros/log/`.


[1]: https://airshipproject.eu
[2]: https://github.com/aslab/sys_self_mc
[3]: https://docs.podman.io/en/latest/
[4]: https://github.com/osrf/docker_images
[5]: https://github.com/ArduPilot/ardupilot/
[6]: https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md
[7]: https://libraibex.com/posts/podman-volumes-permission-denied/
