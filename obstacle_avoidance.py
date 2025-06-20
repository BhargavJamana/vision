import time
import cv2
from picamera2 import Picamera2
from drone_utils import move_forward, move_backward, move_left, move_right, hover, descend
import path_planner

class AdvancedObstacleAvoidance:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": "BGR888", "size": (640, 480)}))
        self.picam2.start()

        self.graph = path_planner.Graph()
        self.setup_map()
        self.current_position = "A"
        self.destination = "C"

    def setup_map(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        self.graph.add_edge("A", "B", 1)
        self.graph.add_edge("B", "C", 1)
        self.graph.add_edge("A", "D", 2)
        self.graph.add_edge("D", "C", 1)

    def detect_obstacle(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, threshold = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return len(contours) > 0

    def move_to_next_node(self, from_node, to_node):
        print(f"Navigating from {from_node} to {to_node}...")
        move_forward(1)
        hover()
        time.sleep(1)

    def follow_path(self, path):
        for i in range(len(path) - 1):
            self.move_to_next_node(path[i], path[i + 1])
            self.current_position = path[i + 1]

    def recalculate_path(self):
        return self.graph.dijkstra(self.current_position, self.destination)

    def prompt_direction(self):
        direction = input("Enter direction (left/right/forward/backward/hover/descend): ").strip().lower()
        distance = int(input("Enter distance in meters: ").strip())

        if direction == "left":
            move_left(distance)
        elif direction == "right":
            move_right(distance)
        elif direction == "forward":
            move_forward(distance)
        elif direction == "backward":
            move_backward(distance)
        elif direction == "hover":
            hover()
        elif direction == "descend":
            descend()
        else:
            print("Invalid direction. Hovering.")
            hover()

    def run(self):
        print("[Advanced Obstacle Avoidance] Live feed started with dynamic path planning...")
        path = self.recalculate_path()
        print("Initial Path:", path)

        while self.current_position != self.destination:
            frame = self.picam2.capture_array()
            cv2.imshow("Live Feed", frame)

            if self.detect_obstacle(frame):
                print("Obstacle detected! Recalculating path...")
                hover()
                time.sleep(2)
                path = self.recalculate_path()
                print("New Path:", path)
                if not path:
                    print("No available path. Hovering...")
                    hover()
                    break
            else:
                self.follow_path(path)
                path = self.recalculate_path()

            if cv2.waitKey(1) & 0xFF == ord('m'):
                self.prompt_direction()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.picam2.stop()
        cv2.destroyAllWindows()

