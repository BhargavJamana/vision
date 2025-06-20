# voice_sender.py
import socket
import speech_recognition as sr

# Update this with your Raspberry Pi IP address
RASPBERRY_PI_IP = "192.168.195.85"  # <-- Replace with your Pi IP
PORT = 8000

# Voice command keywords
VALID_COMMANDS = [
    "take off", "land", "forward", "backward", "left", "right",
    "hover", "stop", "up", "down"
]

def listen_and_send():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("[Laptop] Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)

    while True:
        try:
            with mic as source:
                print("[Laptop] Listening for command...")
                audio = recognizer.listen(source, timeout=5)
            command_text = recognizer.recognize_google(audio).lower()
            print(f"[Laptop] You said: {command_text}")

            for cmd in VALID_COMMANDS:
                if cmd in command_text:
                    print(f"[Laptop] Sending command: {cmd}")
                    send_command(cmd)
                    break
            else:
                print("[Laptop] Command not recognized.")

        except sr.WaitTimeoutError:
            print("[Laptop] Listening timed out.")
        except sr.UnknownValueError:
            print("[Laptop] Could not understand.")
        except sr.RequestError as e:
            print(f"[Laptop] Speech recognition error: {e}")

def send_command(cmd):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((RASPBERRY_PI_IP, PORT))
            s.sendall(cmd.encode())
    except Exception as e:
        print(f"[Laptop] Failed to send: {e}")

if __name__ == "__main__":
    listen_and_send()
