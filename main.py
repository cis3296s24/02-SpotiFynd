import typer
from spotipy.oauth2 import SpotifyClientCredentials
from dataframe import create_dataframe
from filter_features import filter_pitch, filter_tempo, filter_danceability, filter_acousticness, filter_time_signature, filter_liveness, filter_energy
from track_info import get_track_info_and_features, spotify
from save_load import save_filters, load_filters

#spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#spotipy_fix(spotify) #may need to resolve with track_info
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

#Dictionary of filter handlers for filtering in top_tracks, this is used when filtering a song by feature

filter_handlers = {"pitch": filter_pitch, "tempo": filter_tempo, "danceability": filter_danceability,"acousticness": filter_acousticness, "time_signature": filter_time_signature, "liveness": filter_liveness, "energy": filter_energy}

@app.command()
#top_tracks passed arguments based on flags such as -a or -s
def top_tracks(artist: str = typer.Option(None, '-a', '--artist'),
               song: str = typer.Option(None, '-s', '--song'),
               pitch: str = typer.Option(None, '-p', '--pitch'),
               tempo: str = typer.Option(None, '-t', '--tempo'),
               danceability: str = typer.Option(None, '-d', '--dance'),
               time_signature: str = typer.Option(None, '-ts', '--time_signature'),

               acousticness: str = typer.Option(None,'-ac', '--acoustic'),
               liveness: str = typer.Option(None, '-l', '--liveness'),
               energy: str = typer.Option(None, '-e', '--energy'),

               help: str = typer.Option(None, '-h', '--help'),
               save: bool = None,
               load: bool = None,
               ):
    
    if save is not None:
        save_filters(pitch, tempo, danceability, time_signature, acousticness, energy)

    if load is not None:
        pitch, tempo, danceability, time_signature, acousticness, energy = load_filters()
    
    print(r"     _________              __  .__  _____                  .___")
    print(r"    /   _____/_____   _____/  |_|__|/ ____\__.__. ____    __| _/")
    print(r"    \_____  \\____ \ /  _ \   __\  \   __<   |  |/    \  / __ | ")
    print(r"    /        \  |_> >  <_> )  | |  ||  |  \___  |   |  \/ /_/ | ")
    print(r"   /_______  /   __/ \____/|__| |__||__|  / ____|___|  /\____ | ")
    print(r"           \/|__|                         \/         \/      \/ ")
    
    
    if artist is None and song is None:
        
        print("Welcome to SpotiFynd! Please input the artist, song, pitch, tempo, or dance property" + 
          " you are interested in.\nFor example: $python main.py -a 'Drake' -t '120-180' -d '0.2-0.7' -ac '0.4-0.9'" +

          "\n\nThe specific flags are:\n'-a' or 'artist' for artist" +
          "\n\nThe specific flags are: "+
          "\n'-a'  or 'artist'   for artist" +
          "\n'-s'  or '--song'   for song"   +
          "\n'-p'  or '--pitch'  for pitch" +
          "\n'-t'  or '--tempo'  for tempo" + 
          "\n'-d'  or '--dance'  for dance" +
          "\n'-ac' or '--acoust' for acoustic" +
          "\n'-ts' or '--time_signature' for time signature" +
          "\n'-l'  or '--liveness' for liveness" +
          "\n'-e'  or '--energy' for energy" +
          "\n'-h'  or '--help'   for help" +   

          "\nHAVE FUN!")
        

    else:
        
        #Used to filter the search results
        flags = {"artist": artist, "song": song, "pitch": pitch, "tempo": tempo, "danceability": danceability, "acousticness": acousticness, "time_signature": time_signature, "liveness": liveness, "energy": energy}
        
        #artist flag passed limited to 10 results
        if artist:
            search_type = "artist"
            name = artist
        #song flag passed limited by limit= in uri_from_search

        elif song or tempo or pitch or danceability or acousticness or time_signature or energy:
            search_type = "track"
            name = song
        else:
            raise ValueError("You must provide either an artist (-a) or a song (-s).")
        ids = uri_from_search(name, search_type)
        track_data = []
        
        #track search
        if search_type == "track":
            all_info = get_track_info_and_features(ids)
            for track_info, features in all_info:
                #Always append track_info to track_data
                track_data.append(track_info)
                #Apply filters, filter_handlers is a dictionary of filter functions that calls on the filtering functions
                for flag, handler in filter_handlers.items(): 
                    if flags[flag] is not None:
                        #Update the last element of track_data with the filtered track_info
                        track_data[-1] = handler(track_info, features, flags[flag])
        #Artist search
        else:
            for id in ids:
                results = spotify.artist_top_tracks(artist_id=id, country="US")
                track_ids = [track["id"] for track in results["tracks"]]
                if track_ids:
                    all_info = get_track_info_and_features(track_ids) #gets track info and features
                    #for all requested info
                    for track_info, features in all_info:
                        #Operation is always done
                        track_data.append(track_info)
                        #Apply filters
                        for flag, handler in filter_handlers.items():
                            if flags[flag] is not None:
                                track_data[-1] = handler(track_info, features, flags[flag])       
        df = create_dataframe(track_data)


number = float | int


def feature(name: str, minimum: number, maximum: number):
    short_flag = f"-{name[:2]}"
    long_flag = f"--{name}"
    convert = type(minimum)

    # create a custom parser for the inputted audio feature
    def number_range(value: str) -> tuple[number | None, number | None] | number:
        if "-" in value:  # Range provided
            low, high = value.split("-")

            low = convert(low) if low else None
            high = convert(high) if high else None

            if low is not None and low < minimum or high is not None and high > maximum:
                raise ValueError
            return low, high

        # Single value provided
        value = convert(value)
        if not minimum <= value <= maximum:
            raise ValueError
        return value

    return typer.Option(None, short_flag, long_flag, help=f"{minimum} to {maximum}", parser=number_range)


def artists_from_string(string: str) -> list[str]:
    return [uri_from_search(artist.strip(), "artist")[0] for artist in string.split(",")]


def tracks_from_string(string: str) -> list[str]:
    return [uri_from_search(track.strip(), "track")[0] for track in string.split(",")]


def genres_from_string(string: str) -> list[str]:
    return [genre.strip() for genre in string.split(",")]


@app.command(help="""

Search for tracks based on audio features. Note: at least one of {artists, genres, tracks} is required, and their combined total cannot exceed five. 

For all numerical values, you can provide a range with a dash.

For example, --tempo 100-120 will return tracks with a tempo between 100 and 120.

--valence -0.9 will return tracks with a valence at or below 0.9

--loudness 0.4- will return tracks with a loudness at or above 0.4

For artists, genres, and tracks, you can provide a comma-separated list

For example, -a "artist1, artist2" will return tracks by artists similar to artist1 and artist2.
""")
def search(
        limit: int = typer.Option(20, "-l", "--limit", help="Number of results to return."),

        artists: str = typer.Option(None, "-a", "--artists", help="Results will be tracks by similar artists.", parser=artists_from_string),
        genres: str = typer.Option(None, "-g", "--genres", help="Results will be in this genre.", parser=genres_from_string),
        tracks: str = typer.Option(None, "-t", "--tracks", help="Results will be similar to these tracks.", parser=tracks_from_string),

        acousticness=feature("acousticness", 0.0, 1.0),
        danceability=feature("danceability", 0.0, 1.0),
        duration_ms=feature("duration_ms", 0, float("inf")),
        energy=feature("energy", 0.0, 1.0),
        instrumentalness=feature("instrumentalness", 0.0, 1.0),
        key=feature("key", 0, 11),
        liveness=feature("liveness", 0.0, 1.0),
        loudness=feature("loudness", -60.0, 0.0),
        mode=feature("mode", 0, 1),
        popularity=feature("popularity", 0, 100),
        speechiness=feature("speechiness", 0.0, 1.0),
        tempo=feature("tempo", 0.0, float("inf")),
        time_signature=feature("time_signature", 3, 7),
        valence=feature("valence", 0.0, 1.0),
):

    audio_features = {k: v for k, v in locals().items() if k not in {"limit", "artists", "genres", "tracks", "filters"} and v is not None}
    filters = {}

    for audio_feature, value in audio_features.items():
        if isinstance(value, tuple):
            low, high = value
            if low is not None:
                filters[f"min_{audio_feature}"] = low
            if high is not None:
                filters[f"max_{audio_feature}"] = high
        else:
            filters[f"target_{audio_feature}"] = value

    if "popularity" in audio_features:
        del audio_features["popularity"]  # for some reason, Spotify doesn't include this in the returned results

    results = spotify.recommendations(
        seed_artists=artists,
        seed_genres=genres,
        seed_tracks=tracks,
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