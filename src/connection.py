from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import url_for, redirect, session
import time
from config import config

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                           '..', '.env'))
load_dotenv(dotenv_path)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("authorize", _external=True),
        scope="playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-library-read"
    )

def get_token():
    global token_info
    token_info = session.get(config["TOKEN_INFO"], None)
    
    if not token_info:
        raise "exception"
    
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
 
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
 
    return token_info