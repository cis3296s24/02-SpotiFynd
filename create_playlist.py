import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

class Credentials():
    def __init__(self, client_id:str = "", client_secret:str = "", username:str = ""):
        self.client_id = client_id
        self.client_secret=client_secret,
        self.username=username,
        self.redirect_uri="http://localhost:5000",
        self.scope = "playlist-modify-private playlist-modify-public"


def create_playlist(name:str = "test-playlist", is_public:bool = True)->str:
    #Remove later after testing
    client_id = "0e4b89bd47944da690d39e5665b146cc"
    client_secret = "aea56900dd914ebda88809a946993697"
    username = "Gabriel Lopes Carvalho"
    cred = Credentials(client_id, client_secret, username)
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=cred.client_id,
            client_secret=cred.client_secret,
            username=cred.username,
            redirect_uri=cred.redirect_uri,
            scope = cred.scope
        )
    )
    
    exit()
    return sp.user_playlist_create(user=sp.current_user()["id"], name=name, public=is_public)["id"]

def get_playlist()->pd.DataFrame:
    #Remove later after testing
    client_id = "0e4b89bd47944da690d39e5665b146cc"
    client_secret = "aea56900dd914ebda88809a946993697"
    username = "Gabriel Lopes Carvalho"

    cred = Credentials(client_id, client_secret, username)
    cred.scope = "user-top-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=cred.client_id,
            client_secret=cred.client_secret,
            username=cred.username,
            redirect_uri=cred.redirect_uri,
            scope = cred.scope
        )
    )

    results = sp.current_user_top_tracks(limit=10, offset=0,time_range='medium_term')

    track_name = []
    track_id = []
    artist = []
    album = []
    duration = []
    popularity = []
    for i, items in enumerate(results['items']):
            track_name.append(items['name'])
            track_id.append(items['id'])
            artist.append(items["artists"][0]["name"])
            duration.append(items["duration_ms"])
            album.append(items["album"]["name"])
            popularity.append(items["popularity"])

    # Create the final df   
    df = pd.DataFrame({ "track_name": track_name, 
                                "album": album, 
                                "track_id": track_id,
                                "artist": artist, 
                                "duration": duration, 
                                "popularity": popularity})

    return df


if __name__ == "__main__":
    create_playlist()
    