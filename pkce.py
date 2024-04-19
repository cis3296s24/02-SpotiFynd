import spotipy

from spotipy_fix import spotipy_fix

auth_m = spotipy.SpotifyPKCE(client_id="52bd7638025f4ce088463655b18efc50",
                             redirect_uri="http://localhost:8888/callback/",
                             scope="user-library-read user-top-read playlist-modify-public playlist-modify-private")

spotify = spotipy.Spotify(auth_manager=auth_m)
spotipy_fix(spotify)

results = spotify.current_user_top_tracks()

print(results)