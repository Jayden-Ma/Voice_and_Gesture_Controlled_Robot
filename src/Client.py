import socket
import cv2
import mediapipe as mp
import math
import time
import tkinter as tk
import speech_recognition as sr
import pyttsx3

PI_IP = "0.0.0.0"
PORT = 5000

speechMode = False

# Function to recognize speech commands
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening for command...")
        
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)      
            #print(f"Recognized command: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def toggle_speech_mode():
    pass
    
# Function to be called when the button is clicked
def start_program():
    global speed
    speed = speed_var.get()  # Get the value from the slider
    root.destroy()  # Close the tkinter window
    
#Initialize the speech recognizer
recognizer = sr.Recognizer()
# Initialize the tkinter window
root = tk.Tk()
root.title("Set Speed")

# Variable to hold the speed
speed_var = tk.DoubleVar(value=1.0)  # Default speed

# Create a slider for speed
speed_slider = tk.Scale(root, from_=200, to=1200, resolution=0.1, label='Speed', orient='horizontal', variable=speed_var)
speed_slider.pack()

# Create a button to start the program
start_button = tk.Button(root, text="Start", command=start_program)
start_button.pack()

toggle_button = tk.Button(root, text="Toggle Speech Mode", command=toggle_speech_mode)
toggle_button.pack()

# Run the tkinter main loop
root.mainloop()

# Connect to Pi
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((PI_IP, PORT))
print("Connected to PiCar-X!")
print("Use your hands like a steering wheel. Press 'q' to quit.\n")

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

# Helper: compute angle of wrist-to-wrist line
def compute_angle(left, right):
    dx = right.x - left.x
    dy = right.y - left.y
    angle = math.degrees(math.atan2(dy, dx))
    return angle

cap = cv2.VideoCapture(0)

last_sent = ""
cooldown = 0

cmd = f"speed:{speed}"
s.sendall(cmd.encode())
print("Sent:", cmd)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if not speechMode:
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
            # Identify left and right hands by x-position
            hand1, hand2 = results.multi_hand_landmarks
            if hand1.landmark[0].x < hand2.landmark[0].x:
                left_hand = hand1
                right_hand = hand2
            else:
                left_hand = hand2
                right_hand = hand1

            # Get wrist landmarks
            lw = left_hand.landmark[0]
            rw = right_hand.landmark[0]

            # Draw hands
            mp_draw.draw_landmarks(frame, left_hand, mp_hands.HAND_CONNECTIONS)
            mp_draw.draw_landmarks(frame, right_hand, mp_hands.HAND_CONNECTIONS)

            # Compute wheel rotation
            angle = compute_angle(lw, rw)

            # Normalize angle to -90..+90
            if angle > 90:
                angle -= 180
            if angle < -90:
                angle += 180

            # Display angle
            cv2.putText(frame, f"Wheel Angle: {int(angle)}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # Decide commands
            cmd = None
            if abs(angle) < 15:
                cmd = "forward"
            elif angle > 15:
                cmd = "left"
            elif angle < -15:
                cmd = "right"

            s.sendall(cmd.encode())
            print("Sent:", cmd)
            last_sent = cmd
            cooldown = 5 # small delay to reduce spam

        else:
            cv2.putText(frame, "Show Both Hands!", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            # Auto-stop if hands disappear
            if last_sent != "stop":
                s.sendall("stop".encode())
                last_sent = "stop"
                print("Sent: stop")

        # Reduce cooldown
        cooldown -= 1

        cv2.imshow("Steering Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        command = recognize_speech()
        if command is not None:
            print(f"Command received: {command}")
            s.sendall(command.encode())
            print("Sent:", command)
        


# Cleanup
cap.release()
cv2.destroyAllWindows()
s.close()
