import random
import time
from drone_utils import move_up, move_down, hover

def run():
    print("[Terrain Following - SIMULATED] Measuring ground distance...")
    try:
        while True:
            dist = random.choice([30, 45, 70])
            print(f"Distance: {dist} cm")
            if dist < 40:
                move_up()
            elif dist > 60:
                move_down()
            else:
                hover()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped terrain following")