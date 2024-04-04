import json
import os
import spotipy
import typer
from spotipy.oauth2 import SpotifyClientCredentials
from dataframe import create_dataframe
from skip_auth import access_token

# Doesn't allow personal features such as playlist access, 
# but removes the need for username/password.
# Could be a launch option in the future?
spotify = spotipy.Spotify(auth=access_token())

#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
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

#Retrieves track information and features from the Spotify API
def get_track_info_and_features(ids: list):
    results = spotify.tracks(ids) #for artist, song, album
    features = spotify.audio_features(ids) #for tempo, pitch, etc
    all_info = [] #list of both track info and features

    for i in range(len(ids)):
        track_info = {
            "Art": results["tracks"][i]["album"]["images"][0]["url"],
            "Artist": results["tracks"][i]["artists"][0]["name"], 
            "Song": results["tracks"][i]["name"],
        }
        all_info.append((track_info, features[i])) #appends track info and features to all_info

    return all_info

@app.command()
#top_tracks passed arguments based on flags such as -a or -s
def top_tracks(artist: str = typer.Option(None, '-a', '--artist'),
               song: str = typer.Option(None, '-s', '--song'),
               pitch: str = typer.Option(None, '-p', '--pitch'),
               tempo: str = typer.Option(None, '-t', '--tempo'),
               danceabillity: str = typer.Option(None, '-d', '--dance'),
               save: bool = None,
               load: bool = None,
):

    if save is not None:
        saved_filters = {}
        if tempo is not None:
            saved_filters["tempo"] = tempo
        if pitch is not None:
            saved_filters["pitch"] = pitch
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(saved_filters, file, ensure_ascii=False, indent=4)
        return

    if load is not None:
        if not os.path.exists("data.json"):
            raise ValueError("No saved filter. Create one with --save")
        with open("data.json", "r") as file:
            data = json.load(file)
            pitch = data.get("pitch")
            tempo = data.get("tempo")


    print(r"     _________              __  .__  _____                  .___")
    print(r"    /   _____/_____   _____/  |_|__|/ ____\__.__. ____    __| _/")
    print(r"    \_____  \\____ \ /  _ \   __\  \   __<   |  |/    \  / __ | ")
    print(r"    /        \  |_> >  <_> )  | |  ||  |  \___  |   |  \/ /_/ | ")
    print(r"   /_______  /   __/ \____/|__| |__||__|  / ____|___|  /\____ | ")
    print(r"           \/|__|                         \/         \/      \/ ")
    
    #artist flag passed limited to 10 results
    if artist:
        search_type = "artist"
        name = artist
    #song flag passed limited by limit= in uri_from_search
    elif song or tempo or pitch or danceabillity:
        search_type = "track"
        name = song
    else:
        raise ValueError("You must provide either an artist (-a) or a song (-s).")
    ids = uri_from_search(name, search_type)
    track_data = []
    
    #corresponding to 0-11 value for -p search
    pitch_names = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    
    #track search
    if search_type == "track":
        all_info = get_track_info_and_features(ids)
        for track_info, features in all_info:
            #pitch flag was passed
            if pitch is not None and features["key"] == int(pitch):
                track_info["Pitch"] = pitch_names[features["key"]]
                track_data.append(track_info) #appends track info to track_data for df
            #tempo flag was passed
            if tempo is not None:
                min_tempo, max_tempo = map(float, tempo.split('-'))
                if min_tempo <= features["tempo"] <= max_tempo:
                    track_info["Tempo"] = features["tempo"]
                    track_data.append(track_info) #appends track info to track_data for df
            #danceability flag was passed
            if danceabillity is not None:
                min_dance, max_dance = map(float, danceabillity.split('-'))
                if min_dance < 0.0 or max_dance > 1.0:
                    raise ValueError(f"Danceability outside scope. Values must be between 0 and 1")
                if min_dance <= features["danceability"] <= max_dance:
                    track_info["Danceability"] = features["danceability"]
                    track_data.append(track_info)
            #no flags were passed
            if pitch is None and tempo is None and danceabillity is None:
                track_data.append(track_info)
    #Artist search
    else:
        for id in ids:
            results = spotify.artist_top_tracks(artist_id=id, country="US")
            track_ids = [track["id"] for track in results["tracks"]]
            if track_ids:
                all_info = get_track_info_and_features(track_ids) #gets track info and features
                #for all requested info
                for track_info, features in all_info:
                    #if pitch flag was passed
                    if pitch is not None and features["key"] == int(pitch):
                        track_info["Pitch"] = pitch_names[features["key"]]
                        track_data.append(track_info)
                    #if tempo flag was passed
                    if tempo is not None:
                        min_tempo, max_tempo = map(float, tempo.split('-')) #
                        if min_tempo <= features["tempo"] <= max_tempo:
                            track_info["Tempo"] = features["tempo"]
                            track_data.append(track_info)
                    #if danceability was passed
                    if danceabillity is not None:
                        min_dance, max_dance = map(float, danceabillity.split('-'))
                        if min_dance < 0.0 or max_dance > 1.0:
                            raise ValueError(f"Danceability outside scope. Values must be between 0 and 1")
                        if min_dance <= features["danceability"] <= max_dance:
                            track_info["Danceability"] = features["danceability"]
                            track_data.append(track_info)
                    #if no flags were passed
                    else:
                        track_data.append(track_info)       
    df = create_dataframe(track_data)


AUDIO_FEATURES = {
    "acousticness": float,
    "danceability": float,
    "duration_ms": int,
    "energy": float,
    "instrumentalness": float,
    "key": int,
    "liveness": float,
    "loudness": float,
    "mode": int,
    "speechiness": float,
    "tempo": float,
    "valence": float,
    "popularity": int,
    "time_signature": int,
}


def artists_from_string(string: str) -> list[str]:
    return [uri_from_search(artist.strip(), "artist")[0] for artist in string.split(",")]


def tracks_from_string(string: str) -> list[str]:
    return [uri_from_search(track.strip(), "track")[0] for track in string.split(",")]


def genres_from_string(string: str) -> list[str]:
    return [genre.strip() for genre in string.split(",")]


@app.command(help="""

Search for tracks based on audio features. Note: at least one of {artists, genres, tracks} is required, and their combined total cannot exceed five. 

For all numerical values, you can provide a range with a dash.

For example, -t 100-120 will return tracks with a tempo between 100 and 120.

For artists, genres, and tracks, you can provide a comma-separated list

For example, -a "artist1, artist2" will return tracks by artists similar to artist1 and artist2.
""")
def search(
        limit: int = typer.Option(20, "-l", "--limit", help="Number of results to return."),

        artists: str = typer.Option(None, "-a", "--artists", help="Results will be tracks by similar artists."),
        genres: str = typer.Option(None, "-g", "--genres", help="Results will be in this genre."),
        tracks: str = typer.Option(None, "-t", "--tracks", help="Results will be similar to these tracks."),

        acousticness: str = typer.Option(None, "-ac", "--acousticness", help="0.0 to 1.0"),
        danceability: str = typer.Option(None, "-da", "--danceability", help="0.0 to 1.0"),
        duration_ms: str = typer.Option(None, "-du", "--duration_ms", help="0.0 or more"),
        energy: str = typer.Option(None, "-e", "--energy", help="0.0 to 1.0"),
        instrumentalness: str = typer.Option(None, "-i", "--instrumentalness", help="0.0 to 1.0"),
        key: str = typer.Option(None, "-k", "--key", help="0 to 11"),
        liveness: str = typer.Option(None, "-li", "--liveness", help="0.0 to 1.0"),
        loudness: str = typer.Option(None, "-lo", "--loudness", help="−60.0 to 0.0"),
        mode: str = typer.Option(None, "-m", "--mode", help="0 or 1"),
        popularity: str = typer.Option(None, "-p", "--popularity", help="0 to 100"),
        speechiness: str = typer.Option(None, "-s", "--speechiness", help="0.0 to 1.0"),
        tempo: str = typer.Option(None, "-te", "--tempo", help="0.0 or more"),
        time_signature: str = typer.Option(None, "-ts", "--time_signature", help="3 to 7"),
        valence: str = typer.Option(None, "-v", "--valence", help="0.0 to 1.0"),
):
    seed_artists = artists_from_string(artists) if artists is not None else None
    seed_genres = genres_from_string(genres) if genres is not None else None
    seed_tracks = tracks_from_string(tracks) if tracks is not None else None

    audio_features = set()
    filters = {}
    for audio_feature, value in locals().items():
        if value is None or audio_feature not in AUDIO_FEATURES:
            continue
        conversion = AUDIO_FEATURES[audio_feature]
        audio_features.add(audio_feature)
        if "-" in value:  # Range provided
            minimum, maximum = value.split("-")
            if minimum:
                filters[f"min_{audio_feature}"] = conversion(minimum)
            if maximum:
                filters[f"max_{audio_feature}"] = conversion(maximum)
        else:  # Single value provided
            filters[f"target_{audio_feature}"] = conversion(value)

    results = spotify.recommendations(
        seed_artists=seed_artists,
        seed_genres=seed_genres,
        seed_tracks=seed_tracks,
        limit=limit,
        **filters,
    )

    track_data = []
    for track in results["tracks"]:
        track_info = {
            "Art": track["album"]["images"][0]["url"],
            "Artist": track["artists"][0]["name"],
            "Song": track["name"],
        }
        track_audio_features = spotify.audio_features(track["id"])[0]
        for audio_feature in audio_features:
            track_info[audio_feature] = track_audio_features[audio_feature]
        track_data.append(track_info)

    create_dataframe(track_data)


if __name__ == "__main__":
    app()
