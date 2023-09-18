# api_connection.py
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from flask import url_for, redirect
import pandas as pd

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def create_spotify_oauth(redirect_uri):
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-library-read'
    )

def get_token():
    sp_oauth = create_spotify_oauth(redirect_uri='localhost:5000/authorize/')
    token_info = sp_oauth.get_access_token()
    
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
 
    if is_expired:
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
 
    return token_info

def get_tracks(playlist, token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    all_tracks = sp.playlist_items(playlist_id=playlist)

    return all_tracks

def get_tracks_to_df(tracks):
    data = []
    
    for track in tracks:
        d = {
            'track_id': track['track']['id'],
            'track_name': track['track']['name'],
            'album_id': track['track']['album']['id'],
            'album_name': track['track']['album']['name'],
            'album_date': track['track']['album']['release_date'],
            'artist_ids': [artist['id'] for artist in track['track']['album']['artists']],
            'artist_names': [artist['name'] for artist in track['track']['album']['artists']],
            'artist_number': len(track['track']['album']['artists'][0:]),
            'duration_ms': track['track']['duration_ms'],
            'explicit': track['track']['explicit'],
            'popularity': track['track']['popularity'],
            'preview_url': track['track']['preview_url'],
            'album_cover_640': track['track']['album']['images'][0]['url'],
            'album_cover_300': track['track']['album']['images'][1]['url'],
            'album_cover_64': track['track']['album']['images'][2]['url'],
        }
        
        data.append(d)
    
    return pd.DataFrame(data)

def get_audio_features(track_id, token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])  
    
    audio_features = sp.audio_features(tracks=track_id)
    
    return audio_features

def get_audio_analysis(track_id, token_info):

    sp = spotipy.Spotify(auth=token_info['access_token'])  
    
    audio_analysis = sp.audio_analysis(track_id=track_id)
    
    return audio_analysis
    
