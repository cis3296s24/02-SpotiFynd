import spotipy
import typer
from spotipy.oauth2 import SpotifyClientCredentials
from dataframe import create_dataframe

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
app = typer.Typer()


def uri_from_search(name: str, search_type: str):
    #limit determines amount of results, artist and album are limited to 10 results via API
    results = spotify.search(q=f"{search_type}:" + name, type=search_type, limit=50)
    items = results[search_type + "s"]["items"]
    #prints the amount of results
    print(f"Number of results: {len(items)}")
    if len(items) > 0:
        return [item["id"] for item in items]
    else:
        raise ValueError(f"No {search_type}s found with the name {name}")

@app.command()
#top_tracks passed arguments based on flags such as -a or -s
def top_tracks(artist: str = typer.Option(None, '-a', '--artist'),
               song: str = typer.Option(None, '-s', '--song'),
               pitch: str = typer.Option(None, '-p', '--pitch')):
    #artist flag passed limited to 10 results
    if artist:
        search_type = "artist"
        name = artist
    #song flag passed limited by limit= in uri_from_search
    elif song:
        search_type = "track"
        name = song
    #pitch flag passed. Corresponds to 0-11 value
    elif pitch:
        search_type = "track"
        name = pitch
    else:
        raise ValueError("You must provide either an artist (-a) or a song (-s).")
    ids = uri_from_search(name, search_type)
    track_data = []
    
    #corresponding to 0-11 value for -p search
    pitch_names = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    
    #track search includes search types: song title, pitch,
    if search_type == "track":
        for id in ids:
            if pitch is not None:
                # only pull audio features if pitch if specified
                pitch_feature = spotify.audio_features(id)[0]
                if pitch_feature is not None and pitch_feature["key"] is not None and pitch_feature["key"] == int(pitch):
                    results = spotify.track(id)
                    track_info = {
                        "Art": results["album"]["images"][0]["url"],
                        "Artist": results["artists"][0]["name"], 
                        "Song": results["name"],
                        "Pitch": pitch_names[pitch_feature["key"]]
                    }
                    track_data.append(track_info)
            else:
                results = spotify.track(id)
                track_info = {
                    "Art": results["album"]["images"][0]["url"],
                    "Artist": results["artists"][0]["name"], 
                    "Song": results["name"]
                }
                track_data.append(track_info)
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