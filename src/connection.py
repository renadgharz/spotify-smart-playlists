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

def get_token(redirect_uri):
    sp_oauth = create_spotify_oauth(redirect_uri=redirect_uri)
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

def tracks_to_df(tracks):
    data = []
    
    for track in tracks:
        d = {
            'track_id': track['track']['id'],
            'track_name': track['track']['name'],
            'album_id': track['track']['album']['id'],
            'album_name': track['track']['album']['name'],
            'album_date': track['track']['album']['release_date'],
            'artist_id': [artist['id'] for artist in track['track']['album']['artists']],
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

def audio_features_to_df(tracks):
    data = []
    
    for track in tracks:
        d = {
            'track_id': track['id'],
            'danceability': track['danceability'],
            'energy': track['energy'],
            'key': track['key'],
            'loudness': track['loudness'],
            'mode': track['mode'],
            'speechiness': track['speechiness'],
            'acousticness': track['acousticness'],
            'instrumentalness': track['instrumentalness'],
            'liveness': track['liveness'],
            'valence': track['valence'],
            'tempo': track['tempo'],
            'duration_ms': track['duration_ms'],
            'time_signature': track['time_signature']
        }
        
        data.append(d)
    
    return pd.DataFrame(data)

def get_audio_analysis(track_id, token_info):

    sp = spotipy.Spotify(auth=token_info['access_token'])  
    
    audio_analysis = sp.audio_analysis(track_id=track_id)
    
    return audio_analysis
    
def get_artist_info(artist_id, token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    artist_info = sp.artist(artist_id=artist_id)
    
    return artist_info

def artist_info_to_df(artists):
    data = []
    
    for artist in artists:
        d = {
            'artist_id': artist['id'],
            'artist_name': artist['name'],
            'artist_followers': artist['followers']['total'],
            'artist_popularity': artist['popularity'],
            'artist_genres': [artist['genres']],
            'artist_img_300': artist['images'][0]['url']   
        }
        
        data.append(d)
    
    return pd.DataFrame(data)

def get_album_info(album, token_info):
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    album_info = sp.album(album_id=album)
    
    return album_info

def album_info_td_df(albums):
    data = []
    
    for album in albums:
        d = {
            'album_id': album[0]['id']
        }
    
        data.append(d)
        
    return pd.DataFrame(data)