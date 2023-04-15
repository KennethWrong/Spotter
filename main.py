import os
import time
# import playsound
import speech_recognition as sr
from gtts import gTTS

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print(str(e))
    
    return said


if __name__ == "__main__":
    while True:
        said = get_audio()
        
        if said.lower() == "hello":
            print("Yes?")
    
