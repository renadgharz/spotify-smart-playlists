from flask import Flask, request, url_for, session, redirect
from config import config
from connection import create_spotify_oauth

app = Flask(__name__)
app.config.update(config)

# @app.route("/")
# def home():
#     return None

@app.route("/")
def connect_spotify():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/authorize")
def authorize():
    return redirect(url_for("ssp"))

@app.route("/ssp")
def ssp():
    return "Sucessfully redirected from Spotify."

if __name__ == "__main__":
    app.run()