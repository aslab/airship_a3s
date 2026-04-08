#!/bin/sh
# Ardupilot fixed-wing plane Software In The Loop simulation

ARDUP_PREFIX=`ros2 pkg prefix ardupilot_sitl`
PLANE_PARAMS_PATH=$ARDUP_PREFIX/share/ardupilot_sitl/config/models/plane.parm
DDS_PARAMS_PATH=$ARDUP_PREFIX/share/ardupilot_sitl/config/default_params/dds_udp.parm
SITL_PORT=5501
MAVLINK_PORT=5760  # MAVLink master port.

ros2 launch ardupilot_sitl sitl_dds_udp.launch.py \
	command:=arduplane \
	transport:=udp4 \
	synthetic_clock:=True \
	wipe:=False \
	model:=plane \
	speedup:=1 \
	slave:=0 \
	instance:=0 \
	defaults:=$DDS_PARAMS_PATH,$PLANE_PARAMS_PATH \
	sim_address:=127.0.0.1 \
	master:=tcp:127.0.0.1:$MAVLINK_PORT \
	sitl:=127.0.0.1:$SITL_PORT
