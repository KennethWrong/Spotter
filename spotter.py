import os

import spotipy
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import requests

load_dotenv()

categories = {
    "sadness": ['indie', 'mood', 'sleep', "chill"],
    "joy": ['summer','hip-hop', 'pop'],
    "love": ['christian & gospel', 'indie', 'pop', 'r&b'],
    "anger": ['hip-hop', 'rock'],
    "fear": ['wellness'],
    "surprise": ['hip-hop', 'gaming', 'latin'],
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
        self.current_playlist = self.set_default_playlist()
        
        self.emotion_map = categories
        self.categories_map = self.get_category_id_dic() 
    
    def get_playlist_by_category(self, category="party"):
        playlists = self.sp.category_playlists(category_id=category, limit=5)['playlists']['items'][np.random.randint(0, 5)]
        playlist_id = playlists['id']

        playlist = self.sp.playlist(playlist_id=playlist_id)

        self.current_playlist = playlist
        return playlist
    
    def get_song_from_playlist(self, playlist):
        tracks = playlist['tracks']['items']
        track = tracks[np.random.randint(0, len(tracks))]['track']
        return track
    
    def play_song_by_emotion(self, emotion):
        category_id = self.get_category_id_from_emotion(emotion)
        
        playlist = self.get_playlist_by_category(category_id)
        track = self.get_song_from_playlist(playlist=playlist)

        self.play_song_by_uri(track['uri'])

        return track
    
    def get_category_id_dic(self):
        categories = self.sp.categories(country='US')['categories']['items']
        categories = {c['name'].lower():c['id'] for c in categories}
        return categories
    
    def get_category_id_from_emotion(self, emotion):
        category_name = self.emotion_map.get(emotion, ['chill'])

        category_name = np.random.choice(category_name)
        print(category_name)
        
        category_id = self.categories_map.get(category_name)
        return category_id
        
    def play_next_track(self):
        song = self.get_song_from_playlist(self.current_playlist)
        self.play_song_by_uri(song['uri'])
        return song
    
    def play_previous_track(self):
        self.sp.previous_track()
    
    def pause_music(self):
        self.sp.pause_playback()
    
    def resume_music(self):
        self.sp.start_playback()
    
    def play_song_by_uri(self, uri):
        self.sp.add_to_queue(uri)
        self.sp.next_track()
    
    def get_current_song_playing(self):
        res = self.sp.current_playback()
        if res:
            return res['item']
        
        return res

    def set_default_playlist(self):
        feature_playlist = self.sp.featured_playlists(limit=1)['playlists']
        playlist_uri = feature_playlist['items'][0]['uri']

        detailed_playlist = self.sp.playlist(playlist_uri)
        return detailed_playlist
        
    

if __name__ == "__main__":
    spot = Spotter()
    # spot.play_song_by_emotion("anger")
    # spot.set_default_playlist()