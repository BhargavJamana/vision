import cv2
from drone_utils import move_forward, stop

def run():
    cap = cv2.VideoCapture(0)
    print("[Obstacle Avoidance] Watching for obstacles...")

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

        if cv2.countNonZero(thresh) > 60000:
            print("Obstacle detected!")
            stop()
        else:
            move_forward()

        cv2.imshow("Obstacle Avoidance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()