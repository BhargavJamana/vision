import cv2
import mediapipe as mp
from drone_utils import move_forward, stop, move_left, move_right, move_up, move_down


def run():
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    print("[Gesture Mode] Show your hand to the camera...")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_hands.process(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                wrist = hand_landmarks.landmark[0]  # wrist
                index_tip = hand_landmarks.landmark[8]  # index finger tip

                x_diff = index_tip.x - wrist.x
                y_diff = index_tip.y - wrist.y

                if abs(x_diff) > abs(y_diff):
                    if x_diff > 0.1:
                        move_right()
                    elif x_diff < -0.1:
                        move_left()
                    else:
                        move_forward()
                else:
                    if y_diff < -0.1:
                        move_up()
                    elif y_diff > 0.1:
                        move_down()
                    else:
                        stop()
        else:
            stop()

        cv2.imshow('Gesture Control', frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()