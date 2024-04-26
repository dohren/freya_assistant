import sys
import os.path
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from openai_tts import OpenaiTTS
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://localhost:8888/callback"


def execute_skill(action, values):
    # Authentifizierung bei Spotify
    auth_manager = SpotifyOAuth(client_id=client_id,
                                client_secret=client_secret,
                                redirect_uri=redirect_uri,
                                scope="user-read-playback-state user-modify-playback-state")
    sp = spotipy.Spotify(auth_manager=auth_manager)
    if action == "stop_music":
        sp.pause_playback()
    else:
        song_name = values["song"]
        # Suche das Lied
        results = sp.search(q=song_name, limit=1)
        if results['tracks']['items']:
            # Hole die erste Übereinstimmung
            track_uri = results['tracks']['items'][0]['uri']

            # Spiele das Lied ab
            sp.start_playback(uris=[track_uri])
            print(f"Playing {song_name}")
        else:
            print("Song not found.")


if __name__ == "__main__":
    execute_skill("play_song", {"song": "Erreur Boisseau"})