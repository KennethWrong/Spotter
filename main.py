import os
import time
# import playsound
import speech_recognition as sr
from gtts import gTTS

from emotion_analysis.model import EmotionModel
from spotter import Spotter

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
    emotion_model = EmotionModel()
    spotter = Spotter()

    while True:
        said = get_audio()

        if "hello" in said.lower():
            emotion = emotion_model.get_emotion(said)
            print(emotion)
            spotter.play_song_by_emotion(emotion)