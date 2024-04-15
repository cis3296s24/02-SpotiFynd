import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from dataframe import create_dataframe

class Credentials():
    def __init__(self):
        client_id = input("Provide Client ID: ")
        client_secret = input("Provide Client SECRET: ")
        username = input("Provide Username: ")

        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.redirect_uri = "http://localhost:3000"
        self.scope = ""

cred = Credentials()

def create_playlist(name:str = "test-playlist", is_public:bool = True)->str:
    cred.scope = "playlist-modify-private playlist-modify-public"
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
                                "playlist_public": playlist_public,
                                "playlist_tracks":playlist_tracks})

    return df

def add_to_playlist(playlist_id:str, position:int = 0)->int:
    #Remove later after testing
    cred.scope = "playlist-modify-private playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=cred.client_id,
        client_secret=cred.client_secret,
        username=cred.username,
        redirect_uri=cred.redirect_uri,
        scope = cred.scope
        ))
    songs = []
    with open("df.html", "r", encoding="utf-8") as df:
        uris = df['URI']
        for uri in uris:
            songs.append(uri)
        
    sp.playlist_add_items(playlist_id=playlist_id, items=songs, position=position)
    return 0

"""if __name__ == "__main__":
    new_playlist = create_playlist("Software Design Shits 4")
    print(get_playlists_info().head(10))
    songs = ["spotify:track:3vkQ5DAB1qQMYO4Mr9zJN6",
             "spotify:track:2245x0g1ft0HC7sf79zbYN",
             "spotify:track:3ktTWpYdXrYApH54cBo4Ap"]
    
    add_to_playlist(new_playlist, songs)
    """