import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import requests

load_dotenv()

spotify_client_id = os.getenv("SPOTIPY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
spotify_redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

scope="playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private user-read-email user-read-private user-library-modify user-library-read user-read-currently-playing user-modify-playback-state"

auth_manager = SpotifyClientCredentials(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret
)

sp_oauth = SpotifyOAuth(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    redirect_uri=spotify_redirect_uri,
    scope=scope
    
)

song_uri = "https://open.spotify.com/track/2rd4FH1cSaWGc0ZiUaMbX9?si=db3f19bbc0bf4b41"

sp = spotipy.Spotify(auth_manager=sp_oauth)

sp.add_to_queue(song_uri)

sp.next_track()
