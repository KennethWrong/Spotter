from flask import Flask, request
from flask_cors import CORS

from emotion_analysis.model import EmotionModel
from spotter import Spotter

app = Flask(__name__)
CORS(app)

spotter = Spotter()
emotion_model = EmotionModel()

# Index
@app.route('/get_current_song', methods=["GET"])
def get_current_song():
    current_song = spotter.get_current_song_playing()
    ret = {
        'current-song': current_song
    }
    
    return ret
    

@app.route('/play_next_song', methods=["GET"])
def play_next_song():
    current_song = spotter.play_next_track()
    
    return current_song
    

@app.route('/play_previous_song', methods=["GET"])
def play_previous_song():
    current_song = spotter.play_previous_track()
    
    return current_song
    


# About
@app.route('/analyse_audio', methods=["POST", "GET"])
def analyze_audio():
    res = request.json
    text = res['text']
    emotion = emotion_model.get_emotion(text)
    track = spotter.play_song_by_emotion(emotion)
    track['emotion'] = emotion
    return track

if __name__ == '__main__':
    app.run(debug=True, port=8000)