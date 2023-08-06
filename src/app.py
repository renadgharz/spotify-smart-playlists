from flask import Flask, request, url_for, session, redirect, render_template
from config import config
from connection import create_spotify_oauth, get_token
import spotipy

app = Flask(__name__)
app.config.update(config)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/connect", methods=["POST"])
def connect():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    
    return redirect(auth_url)

@app.route("/authorize")
def authorize():
    sp_oauth = create_spotify_oauth()
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session[config["TOKEN_INFO"]] = token_info
    
    return redirect(url_for("ssp"))

@app.route("/app", methods=["GET", "POST"])
def ssp():
    try:
        token_info = get_token()
    except Exception as e:
        print("User not logged in.")
        return redirect(url_for("home"))
    
    sp = spotipy.Spotify(auth=token_info["access_token"])
    
    return sp.current_user_playlists(limit=20, offset=0)['items']

if __name__ == "__main__":
    app.run()