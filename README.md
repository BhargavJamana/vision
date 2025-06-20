Vision-Based UAV Control System with Multi-Modal Autonomy

This project implements a multi-modal autonomous drone control system powered by Raspberry Pi and MAVLink. 
It enables intelligent UAV behavior through various vision- and voice-based human interaction modes using 
Python, OpenCV, DroneKit, and MediaPipe.

 Core Capabilities

-  Gesture Control: Real-time hand detection and directional control using MediaPipe and the PiCamera.
-  Voice Control: Command the drone via speech, captured on a laptop microphone and relayed over Wi-Fi to the Raspberry Pi.
-  Advanced Obstacle Avoidance: Detect obstacles through camera vision and dynamically replan the path to avoid collisions.
-  Terrain Following: Maintain safe altitude using an ultrasonic sensor (HC-SR04) for ground proximity awareness.
-  GPS Path Following: Navigate between GPS waypoints autonomously using the MAVLink protocol.
-  Main Controller: A CLI-based user interface to switch between autonomous control modes seamlessly.

> Developed by: Bhargav  
> Hardware Stack: Raspberry Pi 4, PiCamera, CrossFlight Flight Controller (MAVLink), Ultrasonic Sensor, LiPo Battery  
> Software Stack: Python, OpenCV, DroneKit, MediaPipe, PyMAVLink, Socket Programming

📁 Project Structure

Vision/
│
├── main_controller.py         # Master control panel for mode selection
├── drone_utils.py             # All drone commands (takeoff, land, move, etc.)
│
├── gesture_control.py         # Gesture detection + control with PiCamera
├── voice_control.py           # Local voice command processing
├── obstacle_avoidance.py      # Color-based object detection + path planning
├── terrain_following.py       # Altitude control using ultrasonic data
├── gps_path_following.py      # Autonomous GPS waypoint navigation
│
├── voice_sender.py            # (Laptop) Sends voice commands to Raspberry Pi
├── voice_receiver.py          # (Pi) Receives voice command and executes
│
└── README.md                  # Project documentation

----------------------------------------------------------------------------

 1. Features

| Mode                  | Description                                     |
|-----------------------|-------------------------------------------------|
| Gesture Control       | Move the drone using hand position              |
| Voice Control         | Speak to command: take off, land, move, etc.    |
| Obstacle Avoidance    | Detect obstacles and reroute automatically      |
| Terrain Following     | Adjust altitude based on ground proximity       |
| GPS Path Following    | Follow predefined GPS waypoints                 |
| Central Controller    | Easy CLI-based control interface                |

2. Libraries & Tools

| Library             | Purpose                                        |
|---------------------|------------------------------------------------|
| `dronekit`          | MAVLink-based UAV control                      |
| `pymavlink`         | Low-level MAVLink communication                |
| `opencv-python`     | Real-time camera feed processing               |
| `mediapipe`         | Gesture recognition via hand tracking          |
| `speechrecognition` | Speech-to-text voice command recognition       |
| `RPi.GPIO`          | GPIO pin access for ultrasonic sensor          |
| `picamera2`         | PiCamera control                               |
| `threading`         | Run control modes in parallel                  |
| `socket`            | TCP socket communication for Wi-Fi commands    |

 3. Hardware Components

-> 1. Raspberry Pi 4 (4GB)
-> 2. PiCamera v2.1
-> 3. CrossFlight MAVLink-compatible Flight Controller
-> 4. HC-SR04 Ultrasonic Sensor
-> 5. 3S/4S LiPo Battery
-> 6. Power Resistors (220Ω or 1kΩ for level shifting)
-> 7. USB Data Cable or GPIO TX/RX (UART)

 4. Software Requirements

-> sudo apt update
sudo apt install python3-opencv python3-pip python3-venv python3-picamera2
pip install dronekit pymavlink opencv-python mediapipe speechrecognition pyaudio


 5. Wiring Guide

| Component        | Pin on Pi                       |
|------------------|---------------------------------|
| TRIG (HC-SR04)   | GPIO 23                         |
| ECHO (HC-SR04)   | GPIO 24 (with resistor divider) |
| PiCamera         | CSI Ribbon Port                 |
| Flight Controller| USB (or TELEM via UART)         |

 6.Voice Command Reference

| Command        | Action                  |
|----------------|-------------------------|
| `take off`     | Arms and lifts off      |
| `land`         | Initiates landing       |
| `forward`      | Moves forward           |
| `backward`     | Moves backward          |
| `left/right`   | Strafes left/right      |
| `hover/stop`   | Pauses motion           |
| `up/down`      | Adjusts altitude        |

 7. Voice Control via Wi-Fi

-  `voice_sender.py` (Laptop): Captures and sends command.
-  `voice_receiver.py` (Pi): Receives and executes via MAVLink.
-  Uses socket communication on port `5005` over same Wi-Fi network.
