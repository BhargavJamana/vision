import speech_recognition as sr
import pyttsx3
from drone_utils import takeoff, land, move_forward, stop, get_battery_level

engine = pyttsx3.init()

def speak(text):
    print(f"[Drone]: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_for_command(prompt=None):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        if prompt:
            speak(prompt)
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        speak("I didn't catch that.")
        return None
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return None

def run():
    speak("Voice assistant is active. Say 'drone' to give a command.")

    while True:
        wake = listen_for_command()

        if wake and ("drone" in wake or "hey drone" in wake):
            speak("Yes, How can i assist you.")
            command = listen_for_command("How can i assist?")

            if not command:
                continue

            print(f"Command: {command}")

            if "take off" in command or "takeoff" in command or "fly" in command:
                takeoff()
                speak("Taking off.")

            elif "land" in command:
                land()
                speak("Landing now.")

            elif "forward" in command or "ahead" in command:
                move_forward()
                speak("Moving forward.")

            elif "stop" in command or "halt" in command:
                stop()
                speak("Stopping.")
            elif "retuen home" in command or "alert" in command:
                land()
                speak("returning to home")    

            elif "hello" in command or "hi" in command:
                speak("Hello! I am your drone assistant.")

            elif "battery" in command:
                battery = get_battery_level()
                speak(f"My battery level is {battery} percent.")

            elif "who are you" in command or "about you" in command:
                speak("I am Chitti, the Robo Speed 1 Terahertz Memory 1 Zettabyte")

            else:
                speak("Sorry, I don't understand that command.")
        else:
            print("[Idle] Waiting for wake word...")
