
import cv2
import numpy as np
from drone_utils import send_movement_command

# Define HSV range for red obstacle detection
LOWER_COLOR = np.array([0, 120, 70])
UPPER_COLOR = np.array([10, 255, 255])

# Path grid and simple logic
GRID_SIZE = 10
current_node = (0, 0)

def get_next_node(curr, goal):
    x, y = curr
    gx, gy = goal
    if x < gx:
        return (x + 1, y)
    elif x > gx:
        return (x - 1, y)
    elif y < gy:
        return (x, y + 1)
    elif y > gy:
        return (x, y - 1)
    return curr

def get_direction(curr, nxt):
    cx, cy = curr
    nx, ny = nxt
    if nx > cx:
        return "right"
    elif nx < cx:
        return "left"
    elif ny > cy:
        return "forward"
    elif ny < cy:
        return "backward"
    return "hover"

def detect_obstacle(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_COLOR, UPPER_COLOR)
    return np.sum(mask) > 5000

def obstacle_avoidance_loop(vehicle, stop_flags, goal=(5, 5)):
    global current_node
    cap = cv2.VideoCapture(0)
    print("[OBSTACLE AVOIDANCE] Camera initialized.")

    while not stop_flags["obstacle"]:
        ret, frame = cap.read()
        if not ret:
            print("[OBSTACLE AVOIDANCE] Camera frame not received. Retrying...")
            continue

        if detect_obstacle(frame):
            print("[OBSTACLE] Detected! Hovering...")
            send_movement_command(vehicle, "hover")
            continue

        next_node = get_next_node(current_node, goal)
        direction = get_direction(current_node, next_node)
        print(f"[PATH] Moving {direction} to node {next_node}")
        send_movement_command(vehicle, direction)
        current_node = next_node

        if current_node == goal:
            print("[PATH] Goal reached.")
            send_movement_command(vehicle, "hover")
            break

        cv2.imshow("Obstacle View", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[OBSTACLE AVOIDANCE] Exited.")
