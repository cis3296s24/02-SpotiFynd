import os

import spotipy
from spotipy import Spotify

from credentials import Credentials


def check_auth(spotify: Spotify) -> Spotify:
    if not os.path.exists('credentials.json'):
        print("This command requires account authentication. Please enter below.")
        credentials = Credentials()
        auth = spotipy.SpotifyOAuth(
            client_id=credentials.client_id,
            username=credentials.username,
            client_secret=credentials.client_secret,
            redirect_uri=credentials.redirect_uri,
            scope=credentials.scope
        )
        return spotipy.Spotify(auth=auth)
    return spotify