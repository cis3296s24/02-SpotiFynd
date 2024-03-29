import spotipy
import typer
from spotipy.oauth2 import SpotifyClientCredentials
from dataframe import create_dataframe

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
app = typer.Typer()


def uri_from_artist(name: str):
    results = spotify.search(q="artist:" + name, type="artist")
    items = results["artists"]["items"]
    if len(items) > 0:
        return items[0]["id"]
    else:
        raise ValueError(f"No artists found with the name {name}")


@app.command()
def top_tracks(artist: str):
    results = spotify.artist_top_tracks(artist_id=uri_from_artist(artist), country="US")
    track_data = [
        {
        #always displayed information
        "Art": track["album"]["images"][0]["url"],
        "Artist": track["artists"][0]["name"], 
        "Song": track["name"] 
        }
        for track in results["tracks"]
    ]
    df = create_dataframe(track_data)

if __name__ == "__main__":
    app()
