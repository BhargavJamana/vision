import threading
from dronekit import connect
from gesture_control import run_gesture_control
from voice_control import voice_control_loop
from obstacle_avoidance import obstacle_avoidance_loop
from terrain_following import terrain_following_loop
from gps_path_following import gps_path_following

stop_flags = {
    "gesture": False,
    "voice": False,
    "obstacle": False,
    "terrain": False,
    "gps": False
}

print("[MAIN] Connecting to vehicle...")
vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=57600)
print("[MAIN] Connected to vehicle.")

def stop_all_modes():
    for key in stop_flags:
        stop_flags[key] = True
    import time
    time.sleep(2)
    for key in stop_flags:
        stop_flags[key] = False

def main_menu():
    while True:
        print("\n========== UAV MODE MENU ==========")
        print("1. Gesture Control")
        print("2. Voice Control")
        print("3. Obstacle Avoidance with Path Planning")
        print("4. Terrain Following")
        print("5. GPS Path Following")
        print("6. Exit")
        print("===================================")
        choice = input("Enter your choice: ")

        stop_all_modes()

        if choice == "1":
            print("[MAIN] Starting Gesture Control...")
            threading.Thread(target=run_gesture_control, args=(vehicle, stop_flags)).start()

        elif choice == "2":
            print("[MAIN] Starting Voice Control...")
            threading.Thread(target=voice_control_loop, args=(vehicle, stop_flags)).start()

        elif choice == "3":
            print("[MAIN] Starting Obstacle Avoidance...")
            threading.Thread(target=obstacle_avoidance_loop, args=(vehicle, stop_flags)).start()

        elif choice == "4":
            print("[MAIN] Starting Terrain Following...")
            threading.Thread(target=terrain_following_loop, args=(vehicle, stop_flags)).start()

        elif choice == "5":
            print("[MAIN] Starting GPS Path Following...")
            threading.Thread(target=gps_path_following, args=(vehicle, stop_flags)).start()

        elif choice == "6":
            print("[MAIN] Exiting system...")
            stop_all_modes()
            vehicle.close()
            break

        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n[MAIN] Interrupted. Shutting down.")
        stop_all_modes()
        vehicle.close()
