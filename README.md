## Group project: Jayden Ma, Manpreet, Lucas


*Note: For this project, you will need a separate client computer to connect to the Pi spider*

### Running the Code:
+ First, ensure that the Pi Robot and the client computer are on the same local area network.
+ Also, ensure that mediapipe is properly installed in the project virtual environment
+ To start the server on the Pi Crawler by navigating to home -> pi -> ezb-pi -> workspace. Then run the python server code using `sudo python3 PiServer.py`
    + You can SSH onto the crawler using `ssh pi@<crawlers IP addr>` to make this step easier
+ Now run the client code on the client computer (can be through an IDE or on the command line)
+ Once connected, you can begin using the hand gestures.


### Project Description:
We programmed a remote controlled Pi Crawler that can be controlled using voice commands and hand gestures. The novelty of the system is in our approach. We wanted to design a system where you could easily control the robot from anywhere in the world. To do this, we made the robot a server that client computers can connect to and control the movement of the device.

Another novel feature is the ability to steer the robot with just your voice or hand gestures. There are very few systems that allow users to control remote robits and steer them in real time. 

### Voice Commands:
All voice commands must begin with the activation phrase "Hello Spider". Once the activation phrase has been said, the robot begins listening for commands. The commands we have implemented include:
- move forward
- move left
- move right
- move backwards
- start moving


The user can say "Stop" to cancel the current action.

### Gestures: 
We really wanted to go all in for the gesture implementation. Most gestures are unintuitive and require existing knowledge to use the system. They also don't provide fine-tuned steering and adjustment. Our system uses an innovative and unique steering action instead. 

