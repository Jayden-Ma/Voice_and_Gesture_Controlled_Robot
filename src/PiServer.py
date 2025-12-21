# How to use crawler actions (for reference):
    # Forward ('forward'):
    # Backward ('backward'):
    # Turn Left ('turn left')
    # Turn Right ('turn right')
    # Turn Left Angle ('turn left angle')
    # Turn Right Angle ('turn right angle')
    # Stand ('stand')

from spider import Spider
from ezblock import delay
import socket

# Initialize Spider robot
__SPIDER__ = Spider([10,11,12,4,5,6,1,2,3,7,8,9])

global speed
speed = 400 # any integer up to the max speed of 1200.

global steps
steps = 1 # number of steps to move per command

HOST = "0.0.0.0"
PORT = 5000

__SPIDER__.do_action('stand', 1, speed)

#print(f"Starting server on port {PORT}...")
print ("Starting server on port", PORT)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)

    conn, addr = s.accept()
    print("Connected by", addr)

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            cmd = data.decode().strip()
            print("Received:", cmd)
            cmd_parts = cmd.split(":")
            command = cmd_parts[0]
            steps = int(float(cmd_parts[1])) if len(cmd_parts) > 1 else 1

            if command == "forward":
                __SPIDER__.do_action('forward', steps, speed)

            elif command == "backward":
                __SPIDER__.do_action('backward', steps, speed)

            elif command == "left":
                __SPIDER__.do_action('turn left', steps, speed)

            elif command == "right":
                __SPIDER__.do_action('turn right', steps, speed)
            elif command == "dance":
                __SPIDER__.do_action('forward', 2, speed)
                __SPIDER__.do_action('look_left', 1, speed)
                __SPIDER__.do_action('look_right', 1, speed)
                for count in range(1):
                    __SPIDER__.do_action('look_left', 1, speed)
                    __SPIDER__.do_action('look_right', 1, speed)
                for count2 in range(1):
                    __SPIDER__.do_action('stand', 1, speed)
                    __SPIDER__.do_action('sit', 1, speed)
                __SPIDER__.do_action('push_up', 1, speed)
                __SPIDER__.do_action('backward', 1, speed)
                __SPIDER__.do_action('twist', 1, speed)
                
            elif cmd.startswith("speed"):
                speed = float(cmd.split(":")[1])
                print("Speed:", speed)
            
            else:
                print("Unknown command:", cmd)
