from flask import Flask, request, url_for, session, redirect
from dotenv import load_dotenv
import spotipy
import os
import time
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()

app = Flask(__name__)
app.secret_key = "d8dw7dh"
app.config["SESSION_COOKIE_NAME"] = "login-session"
TOKEN_INFO = "filler"

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

@app.route("/")
def login():
    auth_url = create_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect")
def redirectPage():
    session.clear()
    code = request.args.get("code")
    token_info = create_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("getSongs", _external=True))

@app.route("/getSongs")
def getSongs():
    try:
        token_info = get_token()
    except:
        print("Not logged in")
        return redirect(url_for("login", _external=False))
    
    sp = spotipy.Spotify(auth=token_info["access_token"])
    
    listeningHistory = []
    #print(sp.current_user_saved_tracks(limit=50)['items'])
    resp = sp.current_user_recently_played(limit=50, after=None, before=None)["items"]
    # for song in resp:
    #     artistName = song["track"][1]
    #     songTitle = song["name"]
    #     listeningHistory.append((artistName, songTitle))
    print(resp["tracks"]["artists"]["name"])
    return resp

# check if access token has expired. If so, get new one

def get_token():
    token_info = session.get(TOKEN_INFO)
    if not token_info:
        raise "Exception"
    
    currentTime = int(time.time())
    has_expired = token_info["expires_at"] - currentTime < 60

    if has_expired:
        sp_oauth = create_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])

    return token_info

def create_oauth():
    # returns an obj
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-read-recently-played"
    )