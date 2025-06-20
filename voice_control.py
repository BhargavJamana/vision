import speech_recognition as sr
from drone_utils import send_movement_command, arm_and_takeoff, land, stop

# Command mapping
COMMANDS = {
    "take off": "takeoff",
    "land": "land",
    "forward": "forward",
    "backward": "backward",
    "left": "left",
    "right": "right",
    "hover": "hover",
    "stop": "stop",
    "up": "up",
    "down": "down"
}

def recognize_voice_command(recognizer, audio):
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"[VOICE] You said: {command}")
        for key in COMMANDS:
            if key in command:
                return COMMANDS[key]
        print("[VOICE] Command not recognized.")
        return None
    except sr.UnknownValueError:
        print("[VOICE] Could not understand audio.")
    except sr.RequestError as e:
        print(f"[VOICE] Could not request results; {e}")
    return None

def voice_control_loop(vehicle, stop_flags):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("[VOICE CONTROL] Say a command (e.g., take off, land, forward)...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while not stop_flags["voice"]:
        try:
            with mic as source:
                print("[VOICE] Listening...")
                audio = recognizer.listen(source, timeout=5)
                command = recognize_voice_command(recognizer, audio)

                if command:
                    if command == "takeoff":
                        arm_and_takeoff(3)
                    elif command == "land":
                        land()
                    elif command == "stop":
                        stop()
                    else:
                        send_movement_command(vehicle, command)
        except sr.WaitTimeoutError:
            print("[VOICE] Listening timeout. Retrying...")

    print("[VOICE CONTROL] Deactivated.")


