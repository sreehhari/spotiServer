import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask,jsonify,request,redirect
from flask_cors import CORS
from dotenv import load_dotenv



load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URL = os.getenv('REDIRECT_URL')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URL,
    scope="user-read-recently-played"
))

app=Flask(__name__)

@app.route('/recent-track',methods=['GET'])
def get_recent_track():
    recent_tracks = sp.current_user_recently_played(limit=1)
    if recent_tracks["items"]:
        last_track = recent_tracks["items"][0]["track"]
        output = {
            "name":last_track["name"],
            "artists":[artist["name"] for artist in last_track["artists"]],
            
        }
        return jsonify(output)
    else:
        return jsonify({"error":"no recently played track found"}),404
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)