import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

class Credentials():
    def __init__(self, client_id, client_secret, username):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.redirect_uri = "http://localhost:5000"
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
    return sp.user_playlist_create(user=sp.current_user()["id"], name=name, public=is_public)["id"]

def get_playlists_info()->pd.DataFrame:
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

    results = sp.current_user_playlists(limit=10, offset=0)
    playlist_name = []
    playlist_id = []
    playlist_public = []
    playlist_tracks = []
    for item in results["items"]:
        playlist_name.append(item["name"])
        playlist_id.append(item["id"])
        playlist_public.append(item["public"])
        playlist_tracks.append(item["tracks"])

    # Create the final df   
    df = pd.DataFrame({ "playlist_name": playlist_name, 
                                "playlist_id": playlist_id, 
                                "playlist_public": playlist_public,})

    return df

def add_to_playlist(playlist_id:str, song_uri:list, position:int = 0)->int:
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

    sp.playlist_add_items(playlist_id=playlist_id, items=song_uri, position=position)



if __name__ == "__main__":
    new_playlist = create_playlist("Software Design Shits 2")
    print(get_playlists_info().head(10))
    songs = ["spotify:track:3vkQ5DAB1qQMYO4Mr9zJN6",
             "spotify:track:2245x0g1ft0HC7sf79zbYN",
             "spotify:track:3ktTWpYdXrYApH54cBo4Ap"]
    
    add_to_playlist(new_playlist, songs)
    