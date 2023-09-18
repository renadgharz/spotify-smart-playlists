# app.py
from flask import Flask, request, url_for, session, redirect, render_template
from config import config
from connection import create_spotify_oauth, get_token, get_tracks

app = Flask(__name__)
app.config.update(config)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/connect', methods=['POST'])
def connect():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    
    return redirect(url_for('ssp'))

@app.route('/app', methods=['GET', 'POST'])
def ssp():
    try:
        token_info = session.get('token_info')
        if not token_info:
            raise Exception('User not logged in.')
        
        playlist_id = '5vpQYHxtoC0cy8GZMLQ35g'  # Update with your playlist ID
        
        tracks = get_tracks(playlist_id, token_info)
        
        return tracks

    except Exception as e:
        print('Error:', str(e))
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
