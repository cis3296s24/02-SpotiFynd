import spotipy
import typer
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
app = typer.Typer()


def uri_from_artist(name: str):
    results = spotify.search(q="artist:" + name, type="artist")
    items = results["artists"]["items"]
    if len(items) > 0:
        return items[0]["id"]


@app.command()
def top_tracks(artist: str):
    results = spotify.artist_top_tracks(artist_id=uri_from_artist(artist), country="US")
    for track in results["tracks"]:
        print(track["name"])


if __name__ == "__main__":
    app()
