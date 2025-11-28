from spider import Spider
from ezblock import delay
import socket

# Initialize Spider robot
__SPIDER__ = Spider([10,11,12,4,5,6,1,2,3,7,8,9])

speed = 100

HOST = "0.0.0.0"
PORT = 5000

print(f"Starting server on port {PORT}...")

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

            if cmd == "forward":
                __SPIDER__.do_action('forward', 1, speed)

            elif cmd == "backward":
                __SPIDER__.do_action('backward', 1, speed)

            elif cmd == "left":
                __SPIDER__.do_action('turn left', 1, speed)

            elif cmd == "right":
                __SPIDER__.do_action('turn right', 1, speed)

            else:
                print("Unknown command:", cmd)
