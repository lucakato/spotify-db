from flask import Flask, request, url_for, session, redirect
from dotenv import load_dotenv
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()

app = Flask(__name__)
app.secret_key = "d8dw7dh"
app.config["SESSION_COOKIE_NAME"] = "Luca"

@app.route("/")
def login():
    auth_url = create_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect")
def redirectPage():
    return "redirect"

@app.route("/getSongs")
def getSongs():
    return "Track uno"

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def create_oauth():
    # returns an obj
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-library-read"
    )