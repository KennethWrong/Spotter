import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import requests

load_dotenv()

categories = {
    "anger": [],
    "disgust": [],
    "fear": [],
    "joy": [],
    "neutral": [],
    "sadness": [],
    "surprise": [],
}

spotify_client_id = os.getenv("SPOTIPY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
spotify_redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

class Spotter:
    def __init__(self):
        scope="playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private user-read-email user-read-private user-library-modify user-library-read user-read-currently-playing user-modify-playback-state"

        sp_oauth = SpotifyOAuth(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri=spotify_redirect_uri,
            scope=scope
        )

        self.sp = spotipy.Spotify(auth_manager=sp_oauth)
    
    def get_song_by_category(self, category="party"):
        res = self.sp.categories()['categories']['items']
        res = [r['name'] for r in res]
        print(res)



if __name__ == "__main__":
    spot = Spotter()
    spot.get_song_by_category()