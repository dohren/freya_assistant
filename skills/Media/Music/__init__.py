import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from openai_tts import OpenaiTTS
import spotipy
from spotipy.oauth2 import SpotifyOAuth




def execute_skill(action, values):
    song_name = values["song"]
    # Authentifizierung bei Spotify
    auth_manager = SpotifyOAuth(client_id=client_id,
                                client_secret=client_secret,
                                redirect_uri=redirect_uri,
                                scope="user-read-playback-state user-modify-playback-state")
    sp = spotipy.Spotify(auth_manager=auth_manager)

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