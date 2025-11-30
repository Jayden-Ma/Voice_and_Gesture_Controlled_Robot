import speech_recognition as sr
import pyttsx3

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def recognize_speech():
    while(1):
        with sr.Microphone() as source:
            print("Listening for command...")
        
            try:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)      
                print(f"Recognized command: {command}")
                return command
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None
            
while(1):
    command = recognize_speech()
    if command is not None:
        print(f"Command received: {command}")
