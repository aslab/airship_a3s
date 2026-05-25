import launch
import launch_ros

# TODO: there seems to be an issue with the time syncronization
# [mavros_node-4] [WARN] [mavros.time]: TM: Wrong FCU time.
# [mavros_node-4] [INFO] [mavros.time]: TM: Timesync mode: MAVLINK
# [mavros_node-4] [WARN] [mavros.time]: TM: RTT too high for timesync: 19.27 ms.
def generate_launch_description() -> launch.LaunchDescription:
    ardupilot_prefix = "/home/oper/fms/install/ardupilot_sitl/"
    plane_params = ardupilot_prefix + "share/ardupilot_sitl/config/models/plane.parm"
    dds_params = ardupilot_prefix + "share/ardupilot_sitl/config/default_params/dds_udp.parm"
    default_params_paths = plane_params + "," + dds_params

    return launch.LaunchDescription(
        [
            launch.actions.IncludeLaunchDescription(
                launch.substitutions.PathJoinSubstitution(
                    [
                        launch_ros.substitutions.FindPackageShare("ardupilot_sitl"),
                        "launch",
                        "sitl_dds_udp.launch.py"
                    ]
                ),
                launch_arguments={
                    "command": "arduplane",
                    	"synthetic_clock": "True",
	                "wipe": "False",
	                "model": "plane",
	                "speedup": "1",
	                "slave": "0",
	                "instance": "0",
	                "defaults": default_params_paths,
	                "sim_address": "127.0.0.1",
	                "master": "tcp:127.0.0.1:5760",
	                "sitl": "127.0.0.1:5501"
	            }.items()
            ),
            launch.actions.IncludeLaunchDescription(
                launch.substitutions.PathJoinSubstitution(
                        [
                            launch_ros.substitutions.FindPackageShare("mavros"),
                            "launch",
                            "apm.launch"
                        ]
                ),
                launch_arguments={
                    "fcu_url": "udp://0.0.0.0:14550@",
                    "config_yaml": "apm_config.yaml",
                    "pluginlists_yaml": "apm_pluginlists.yaml"
                }.items()
            ),
            launch_ros.actions.Node(
                package="a3s",
                executable="mission",
            )
        ]
    )

