# MAVLink utility functions (placeholder)

from pymavlink import mavutil
import time

# Connect to the flight controller via USB
print("[MAVLink] Connecting to flight controller...")
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600)
master.wait_heartbeat()
print("[MAVLink] Heartbeat received from system (system %u component %u)" %
      (master.target_system, master.target_component))

# Arm and take off
def arm_and_takeoff(altitude):
    print("[Drone] Arming motors...")
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 1, 0, 0, 0, 0, 0, 0)
    time.sleep(2)

    master.set_mode(mavutil.mavlink.MAV_MODE_GUIDED_ARMED)
    print(f"[Drone] Taking off to {altitude} meters...")

    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0, 0, 0, 0, 0, 0, 0, altitude)
    time.sleep(8)

# Land
def land():
    print("[Drone] Landing...")
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0, 0, 0, 0, 0, 0, 0, 0)

# Send NED velocity
def send_ned_velocity(vx, vy, vz, duration):
    print(f"[NED] vx={vx}, vy={vy}, vz={vz} for {duration} seconds")
    for _ in range(duration * 10):
        master.mav.set_position_target_local_ned_send(
            int(time.time() * 1000), master.target_system, master.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            0b0000111111000111, 0, 0, 0,
            vx, vy, vz, 0, 0, 0, 0, 0)
        time.sleep(0.1)

# Directional commands
def move_forward(): send_ned_velocity(1, 0, 0, 2)
def move_backward(): send_ned_velocity(-1, 0, 0, 2)
def move_left(): send_ned_velocity(0, -1, 0, 2)
def move_right(): send_ned_velocity(0, 1, 0, 2)
def ascend(): send_ned_velocity(0, 0, -0.5, 2)
def descend(): send_ned_velocity(0, 0, 0.5, 2)
def hover(): send_ned_velocity(0, 0, 0, 2)

# Stop function (for voice command)
def stop(vehicle=None):
    print("[Drone] Stopping movement.")
    hover()

# Unified command interface
def send_movement_command(master, command, duration=2):
    if command == "forward": move_forward()
    elif command == "backward": move_backward()
    elif command == "left": move_left()
    elif command == "right": move_right()
    elif command == "up": ascend()
    elif command == "down": descend()
    elif command == "hover" or command == "stop": hover()
    else: print("[WARN] Unknown command:", command)
