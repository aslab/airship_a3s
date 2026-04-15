#!/usr/bin/env python3
# A basic fixed-wing drone mission manager.

import time
import typing

import rclpy
import rclpy.node
import rclpy.qos
import mavros_msgs.msg
import mavros_msgs.srv


class MissionManager(rclpy.node.Node):
    """Fixed-wing drone mission manager node"""
    
    def __init__(self):
        super().__init__("mission_manager")

        # Service clients.        
        self.set_home_client = self.create_client(
            mavros_msgs.srv.CommandHome,
            "/mavros/cmd/set_home"
        )
        self.set_mode_client = self.create_client(mavros_msgs.srv.SetMode, "/mavros/set_mode")
        self.clear_waypoints_client = self.create_client(
            mavros_msgs.srv.WaypointClear,
            "/mavros/mission/clear"
        )
        self.waypoint_push_client = self.create_client(
            mavros_msgs.srv.WaypointPush,
            "/mavros/mission/push"
        )
        self.arming_client = self.create_client(mavros_msgs.srv.CommandBool, "/mavros/cmd/arming")

        # Wait for MAVROS services to be up.
        self.get_logger().info("Waiting for MAVROS services...")
        self.wait_for_services()
        self.get_logger().info("MAVROS services availability confirmed.")

    def wait_for_services(self):
        """Wait for the required MAVROS services to be available"""
        for service in (
            self.set_home_client,
            self.set_mode_client,
            self.clear_waypoints_client,
            self.waypoint_push_client,
            self.arming_client
        ):
            while not service.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(f"Waiting for {service.srv_name}...")

    def set_home_current(self):
        """Set home position to current location."""
        request = mavros_msgs.srv.CommandHome.Request()
        request.current_gps = True

        self.get_logger().info("Calling home position service...")
        future = self.set_home_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        result = future.result()
        if result is None:
            raise RuntimeError("Set home service call failed")
        if result.success:
            self.get_logger().info("Home position set to current location")
        else:
            raise RuntimeError(
                f"Failed to set home position. Result from {self.set_home_client.srv_name} "
                f"was {future.result().result}."
            )
    
    def set_mode(self, mode: str):
        """Set flight mode. Either AUTO, LOITER or RTL."""
        if mode not in ("AUTO", "LOITER", "RTL"):
            raise ValueError(f"Error: mode {mode} not supported.")

        request = mavros_msgs.srv.SetMode.Request()
        request.custom_mode = mode

        self.get_logger().info(f"Setting mode to {mode}...") 
        future = self.set_mode_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        result = future.result()
        if result is None:
            raise RuntimeError("Set mode service call failed")
        if result.mode_sent:
            self.get_logger().info(f"Mode correctly changed to {mode}.")
        else:
            raise RuntimeError(f"Failed to set mode {mode}.")

    def clear_mission(self):
        """Clear all waypoints from the autopilot."""
        request = mavros_msgs.srv.WaypointClear.Request()
        
        self.get_logger().info("Clearing all waypoints from autopilot...")
        future = self.clear_waypoints_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        result = future.result() 
        if result is None:
            raise RuntimeError("WaypointClear service call failed")
        if result.success:
            self.get_logger().info("Mission cleared successfully.")
        else:
            raise RuntimeError(f"Failed to clear mission.")

    def create_basic_mission(self) -> typing.List[mavros_msgs.msg.Waypoint]:
        """Creates a basic mission: Home, takeoff, loiter"""
        waypoints = []
        
        # Waypoint 0: Home position (required).
        waypoint = mavros_msgs.msg.Waypoint()
        waypoint.frame = 0  # MAV_FRAME_GLOBAL.
        waypoint.command = 16  # MAV_CMD_NAV_WAYPOINT.
        waypoint.is_current = True
        waypoint.autocontinue = True
        waypoint.x_lat = -35.3632622
        waypoint.y_long = 149.1652374
        waypoint.z_alt = 603.5386372034106
        waypoints.append(waypoint)

        # Waypoint 1: Takeoff.
        waypoint = mavros_msgs.msg.Waypoint()
        waypoint.frame = 0  # MAV_FRAME_LOCAL_ENU.
        waypoint.command = 22  # MAV_CMD_NAV_TAKEOFF.
        waypoint.is_current = False
        waypoint.autocontinue = True
        waypoint.param1 = 15.0  # Minimum/desired pitch in degrees.
        waypoint.x_lat = -35.361730
        waypoint.y_long = 149.164987
        waypoint.z_alt = 613.5
        waypoints.append(waypoint)

        # Waypoint 2: Loiter at poisition.
        waypoint = mavros_msgs.msg.Waypoint()
        waypoint.frame = 0  # MAV_FRAME_LOCAL_ENU.
        waypoint.command = 17  # MAV_CMD_NAV_LOITER_UNLIM.
        waypoint.is_current = False
        waypoint.autocontinue = False
        waypoint.x_lat = -35.359923
        waypoint.y_long = 149.164735
        waypoint.z_alt = 623.5
        waypoints.append(waypoint)
        
        return waypoints

    def push_mission(self, mission: typing.List[mavros_msgs.msg.Waypoint]):
        """Upload waypoints to the autopilot."""
        request = mavros_msgs.srv.WaypointPush.Request()
        request.start_index = 0
        request.waypoints = mission
        
        self.get_logger().info(f"Pushing {len(mission)} waypoints to autopilot...")
        future = self.waypoint_push_client.call_async(request)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)

        result = future.result()
        if result is None:
            raise RuntimeError("WaypointPush service call failed")
        if result.success:
            self.get_logger().info(
                f"{future.result().wp_transfered} mission waypoints succesfully pushed."
            )
        else:
            raise RuntimeError(f"Failed to push mission.")

    def arm(self):
        request = mavros_msgs.srv.CommandBool.Request()
        request.value = True

        self.get_logger().info(f"Arming drone...")
        future = self.arming_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        result = future.result()
        if result is None:
            raise RuntimeError("Arming service call failed")
        if result.success:
            self.get_logger().info("Drone armed succesfully.")
        else:
            raise RuntimeError(f"Failed to arm the drone.")


def run():
    rclpy.init()
    mission_manager = MissionManager()

    try:
        mission_manager.set_home_current()
        time.sleep(1)

        mission_manager.clear_mission()
        time.sleep(1)

        mission = mission_manager.create_basic_mission()
        mission_manager.push_mission(mission)
        time.sleep(1)

        mission_manager.set_mode("AUTO")
        time.sleep(1)

        mission_manager.arm()
        time.sleep(2)

        mission_manager.get_logger().info("Mission running. Press Ctrl+C to finish it.")
        rclpy.spin(mission_manager)
    except KeyboardInterrupt:
        mission_manager.get_logger().info("Flight interrupted by operator")
    except RuntimeError as e:
        mission_manager.get_logger().error(f"RuntimeError: {e}")
    except Exception as e:
        mission_manager.get_logger().error(f"An error occurred: {e}")
    finally:
        mission_manager.destroy_node()
        #rclpy.shutdown()

if __name__ == '__main__':
    run()
