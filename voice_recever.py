import socket
from drone_utils import arm_and_takeoff, land, hover, send_movement_command
from dronekit import connect

# Connect to the flight controller
print("[Pi] Connecting to drone...")
vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=57600)
print("[Pi] Drone connected successfully.")

# Socket setup (TCP)
HOST = ''  # Listen on all interfaces
PORT = 5005
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"[Pi] Listening for voice commands on port {PORT}...")

def handle_command(cmd):
    cmd = cmd.strip().lower()
    print(f"[COMMAND RECEIVED] {cmd}")

    if "take off" in cmd or "takeoff" in cmd:
        arm_and_takeoff(vehicle, 3)
    elif "land" in cmd:
        land(vehicle)
    elif "hover" in cmd or "stop" in cmd:
        hover(vehicle)
    elif cmd in ["forward", "backward", "left", "right", "up", "down"]:
        send_movement_command(vehicle, cmd)
    else:
        print("[Pi] Unknown command received.")

try:
    conn, addr = server.accept()
    print(f"[Pi] Connection established with {addr}")

    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        handle_command(data)

except KeyboardInterrupt:
    print("\n[Pi] Shutting down receiver.")

finally:
    conn.close()
    server.close()
    vehicle.close()
    print("[Pi] Clean shutdown.")
