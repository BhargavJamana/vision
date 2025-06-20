import cv2
from drone_utils import move_forward, stop

def run():
    cap = cv2.VideoCapture(0)
    print("[Follow Me Mode] Show red object to follow...")

    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0, 120, 70), (10, 255, 255))

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            move_forward()
        else:
            stop()

        cv2.imshow("Follow Me", mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()