import spotipy
import typer
from spotipy.oauth2 import SpotifyClientCredentials
from dataframe import create_dataframe

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
app = typer.Typer()


def uri_from_search(name: str, search_type: str):
    results = spotify.search(q=f"{search_type}:" + name, type=search_type)
    items = results[search_type + "s"]["items"]
    if len(items) > 0:
        return [item["id"] for item in items]
    else:
        raise ValueError(f"No {search_type}s found with the name {name}")


@app.command()
def top_tracks(artist: str = typer.Option(None, '-a', '--artist'), song: str = typer.Option(None, '-s', '--song')):
    if song:
        search_type = "track"
        name = song
    elif artist:
        search_type = "artist"
        name = artist
    else:
        raise ValueError("You must provide either an artist (-a) or a song (-s).")
    ids = uri_from_search(name, search_type)
    track_data = []
    if search_type == "track":
        for id in ids:
            results = spotify.track(id)
            track_data.append({
                "Art": results["album"]["images"][0]["url"],
                "Artist": results["artists"][0]["name"], 
                "Song": results["name"] 
            })
    else:
        for id in ids:
            results = spotify.artist_top_tracks(artist_id=id, country="US")
            for track in results["tracks"]:
                track_data.append({
                    "Art": track["album"]["images"][0]["url"],
                    "Artist": track["artists"][0]["name"], 
                    "Song": track["name"] 
                })
    df = create_dataframe(track_data)
if __name__ == "__main__":
    app()