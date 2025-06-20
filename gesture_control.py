import cv2
import mediapipe as mp
from drone_utils import send_movement_command
from picamera2 import Picamera2

def run_gesture_control(vehicle, stop_flags):
    # Initialize PiCamera
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": "BGR888", "size": (640, 480)}))
    picam2.start()

    # MediaPipe Hands
    mp_hands = mp.solutions.hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    print("[Gesture Control] Show your hand to the camera...")

    try:
        while not stop_flags["gesture"]:
            frame = picam2.capture_array()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = mp_hands.process(image)

            # Get current altitude from vehicle
            current_alt = vehicle.location.global_relative_frame.alt
            cv2.putText(frame, f"Altitude: {current_alt:.2f}m", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                    wrist = hand_landmarks.landmark[0]
                    index_tip = hand_landmarks.landmark[8]

                    x_diff = index_tip.x - wrist.x
                    y_diff = index_tip.y - wrist.y

                    if current_alt <= 2.0:
                        cv2.putText(frame, "Gesture Active", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        if abs(x_diff) > abs(y_diff):
                            if x_diff > 0.1:
                                send_movement_command(vehicle, "right")
                            elif x_diff < -0.1:
                                send_movement_command(vehicle, "left")
                            else:
                                send_movement_command(vehicle, "forward")
                        else:
                            if y_diff < -0.1:
                                send_movement_command(vehicle, "up")
                            elif y_diff > 0.1:
                                send_movement_command(vehicle, "down")
                            else:
                                send_movement_command(vehicle, "hover")
                    else:
                        cv2.putText(frame, "Too High for Gesture", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        send_movement_command(vehicle, "hover")
            else:
                send_movement_command(vehicle, "hover")

            cv2.imshow("Live Gesture Camera Feed", frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    finally:
        picam2.stop()
        cv2.destroyAllWindows()
        print("[Gesture Control] Exited.")
