import launch
import launch_ros


def generate_launch_description() -> launch.LaunchDescription:
    fms_prefix = "/home/oper/fms/install/"
    ardupilot_prefix = fms_prefix + "ardupilot_sitl/share/ardupilot_sitl/config/"
    plane_params = ardupilot_prefix + "models/plane.parm"
    dds_params = ardupilot_prefix + "default_params/dds_udp.parm"
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
                    "sitl": "127.0.0.1:5501",
                    "map": "True",
                }.items()
            ),
            launch.actions.IncludeLaunchDescription(
                launch.substitutions.PathJoinSubstitution(
                        [
                            launch_ros.substitutions.FindPackageShare("mavros"),
                            "launch",
                            "node.launch"
                        ]
                ),
                launch_arguments={
                    "fcu_url": "udp://0.0.0.0:14550@",
                    "gcs_url": "",
                    "tgt_system": "1",
                    "tgt_component": "1",
                    "pluginlists_yaml": "apm_pluginlists.yaml",
                    "config_yaml": fms_prefix + "/a3sys/share/a3sys/apm_config.yaml",
                }.items()
            ),
            launch_ros.actions.Node(
                package="a3sys",
                executable="mission",
            )
        ]
    )
