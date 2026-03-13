import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="18c9f2493f8e4bc2851dc9b8632c202a",
    client_secret="70e718f19b804805b835a7dce9719842",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-top-read"
))

results = sp.current_user_top_artists(limit=10)

print("Tus artistas más escuchados:\n")

for artist in results['items']:
    print(artist['name'])
