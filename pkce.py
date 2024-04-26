import json
from requests import Session
from spotipy import Spotify, SpotifyPKCE

#Try to load the client_id from the JSON file
try:
    with open('client_id.json', 'r') as f:
        client_id = json.load(f)
except FileNotFoundError:
    #If the file doesn't exist, prompt the user to enter their client_id
    client_id = input("Please enter your client_id: ")
    #Save the client_id to the JSON file
    with open('client_id.json', 'w') as f:
        json.dump(client_id, f)

redirect_uri = "http://localhost:8888/callback/"
scope = "user-library-read user-top-read playlist-modify-public playlist-modify-private"
state = None

spotify = Spotify(auth_manager=SpotifyPKCE(client_id, redirect_uri, state, scope))

def fixed_del(self):
    if isinstance(self._session, Session):
        self._session.close()

spotify.__del__ = fixed_del.__get__(spotify, Spotify)