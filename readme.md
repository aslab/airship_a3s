Awareness, Anticipation and Adaptation System
=============================================
The environment used to develop, build and test the system will be a container running Ubuntu 22 with ROS 2. The container tool used here is [Podman][1]. Although all container related sources are OCI compliant, so Docker should also work.

The image used will be based on ROS2 Humble taken from the [OSRF Docker images][2]. Building [Ardupilot][3] for our use case.
```sh
cd <project_directory>
podman build --build-arg=BUILD_WORKERS=12 -t custom-ros-core:latest .
```
The `--build-arg=BUILD_WORKERS=12` will configure the build to use 12 parallel jobs to accelerate the compilation. The argument is optional and its value can be changed.

We will create an unprivileged, [rootless container][4]. For the moment, we will run a simple init program (`initcnt`) to keep the container available in the background.
```sh
podman run -d --userns=keep-id -v ./vol:/mnt/vol:Z --hostname=fms --name fms localhost/custom-ros-core:latest initcnt
podman ps  # See the created container is running.
```
Note that to [enable the host-container volume to work with a host OS having SELinux labels for the directories][5] (such as Fedora) we have to append a `:Z` to the volume path.

You can then enter the container with the following command.
```sh
podman exec -it -u root fms login oper  # Login as user "oper".
```
We enter through `login` to initialize the environment as usual, that is, sourcing `~/.profile`, `~/.bashrc` etc. Still, all configuration is intended to place all the setup required in the `~/.bashrc` with the intention of allowing a simpler entrypoint.

Testing
-------
Once the image has been build, you can test that Ardupilot is working correctly by running some tests.
```sh
oper@fms $ cd fms/rosws
oper@fms $ source install/local-setup.bash
oper@fms $ colcon test --executor sequential --base-paths src/ardupilot --event-handlers=console_direct+
```

To test that the SITL works, run the following.
```sh
oper@fms $ mkdir sims
oper@fms $ cd sims
oper@fms $ ln -s /mnt/vol/launchsim.sh launchsim.sh
oper@fms $ ./launchsim.sh
```

Open another terminal, enter the container, run mavproxy and command the aircraft to take off.
```sh
host $ podman exec -it -u root fms login oper
oper@fms $ cd fms/rosws
oper@fms $ source install/local_setup.bash
oper@fms $ mavproxy.py --aircraft test --master=:14550
MANUAL> mode guided
GUIDED> arm throttle
GUIDED> mode takeoff
```
You should see now that the aircraft is gaining height.


[1]: https://docs.podman.io/en/latest/
[2]: https://github.com/osrf/docker_images
[3]: https://github.com/ArduPilot/ardupilot/
[4]: https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md
[5]: https://libraibex.com/posts/podman-volumes-permission-denied/
