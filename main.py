from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"   
    }
    data = {"grant_type": "client_credentials"}
    # post will return a json obj
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# For sending requests to API
# construct header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# returns ID for artist
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search?"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_res = json.loads(result.content)["artists"]["items"]
    if len(json_res) == 0:
        print("Could not find artist")
        return None
    return json_res[0]


def getTopSongsArtist(token, id):
    headers = get_auth_header(token)
    query_url = f"https://api.spotify.com/v1/artists/{id}/top-tracks?country=JP"
    res = get(query_url, headers=headers)
    json_res = json.loads(res.content)["tracks"]
    return json_res

token = get_token()
res = search_for_artist(token, "Carlo Redl")
artist_id = res["id"]
songs = getTopSongsArtist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx+1}. {song['name']}")