import gesture_control
import voice_control
import obstacle_avoidance
import follow_me
import terrain_following

def main():
    print("\n==== UAV Vision Control Modes ====")
    print("1. Gesture Control")
    print("2. Voice Control")
    print("3. Obstacle Avoidance")
    print("4. Follow Me")
    print("5. Terrain Following")
    choice = input("Enter your choice: ")

    if choice == '1':
        gesture_control.run()
    elif choice == '2':
        voice_control.run()
    elif choice == '3':
        obstacle_avoidance.run()
    elif choice == '4':
        follow_me.run()
    elif choice == '5':
        terrain_following.run()
    else:
        print("Invalid option")

if __name__ == '__main__':
    main()