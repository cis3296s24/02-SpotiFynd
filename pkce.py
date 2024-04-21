from requests import Session
from spotipy import Spotify, SpotifyPKCE

client_id = "52bd7638025f4ce088463655b18efc50"  # no need to replace this with your own client_id
redirect_uri = "http://localhost:8888/callback/"  # same for this one
scope = "user-library-read user-top-read playlist-modify-public playlist-modify-private"
state = None

spotify = Spotify(auth_manager=SpotifyPKCE(client_id, redirect_uri, state, scope))

def fixed_del(self):
    if isinstance(self._session, Session):
        self._session.close()


spotify.__del__ = fixed_del.__get__(spotify, Spotify)
