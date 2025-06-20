# Terrain following script (placeholder)
import time
import RPi.GPIO as GPIO
from drone_utils import ascend, descend, hover

# GPIO pin setup
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # Trigger pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    stop = time.time()

    # Wait for echo to start
    while GPIO.input(ECHO) == 0:
        start = time.time()

    # Wait for echo to stop
    while GPIO.input(ECHO) == 1:
        stop = time.time()

    # Time difference
    elapsed = stop - start
    distance = (elapsed * 34300) / 2  # cm
    return round(distance, 2)

def terrain_following_loop(vehicle, stop_flags):
    print("[TERRAIN FOLLOWING] Using Ultrasonic Sensor (HC-SR04)")
    try:
        while not stop_flags["terrain"]:
            distance = get_distance()
            print(f"[TERRAIN] Distance from ground: {distance} cm")

            if distance < 40:
                print("[TERRAIN] Too close, ascending...")
                ascend()
            elif distance > 60:
                print("[TERRAIN] Too high, descending...")
                descend()
            else:
                print("[TERRAIN] Optimal height, hovering...")
                hover()

            time.sleep(1)

    except KeyboardInterrupt:
        print("[TERRAIN FOLLOWING] Interrupted.")

    finally:
        GPIO.cleanup()
        print("[TERRAIN FOLLOWING] Sensor GPIO cleaned up.")
