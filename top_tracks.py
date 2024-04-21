import typer
from save_load import save_filters, load_filters
from utility import uri_from_search
from filter_features import filter_handlers
from track_info import get_track_info_and_features
from dataframe import create_dataframe
from pkce import spotify


def get_top_tracks(artist: str = typer.Option(None, '-a', '--artist'),
                   song: str = typer.Option(None, '-s', '--song'),
                   pitch: str = typer.Option(None, '-p', '--pitch'),
                   tempo: str = typer.Option(None, '-t', '--tempo'),
                   danceability: str = typer.Option(None, '-d', '--dance'),
                   time_signature: str = typer.Option(None, '-ts', '--time_signature'),
                   acousticness: str = typer.Option(None, '-ac', '--acoustic'),
                   liveness: str = typer.Option(None, '-l', '--liveness'),
                   energy: str = typer.Option(None, '-e', '--energy'),
                   speechiness: str = typer.Option(None, '-sp', '--speechiness'),
                   save: bool = None,
                   load: bool = None,
                   ):
    if save is not None:
        save_filters(pitch, tempo, danceability, time_signature, acousticness, energy, speechiness)

    if load is not None:
        pitch, tempo, danceability, time_signature, acousticness, energy, speechiness = load_filters()

    # Used to filter the search results
    flags = {
        "artist": artist,
        "song": song,
        "pitch": pitch,
        "tempo": tempo,
        "danceability": danceability,
        "acousticness": acousticness,
        "time_signature": time_signature,
        "liveness": liveness,
        "energy": energy,
        "speechiness": speechiness
    }

    non_audio_features = {"limit", "artist", "genres", "tracks", "save", "load"}
    searched_audio_features = {k: v for k, v in locals().items() if k not in non_audio_features and v is not None}


    if artist:
        search_type = "artist"
        name = artist
    elif song:
        search_type = "track"
        name = song
    else:
        raise ValueError("You must provide either an artist (-a) or a song (-s).")

    ids = uri_from_search(name, search_type)
    track_data = []

    # track search
    if search_type == "track":
        all_info = get_track_info_and_features(ids)
        for track_info, features in all_info:
            # Always append track_info to track_data
            track_data.append(track_info)
            # Apply filters, filter_handlers is a dictionary of filter functions that calls on the filtering functions
            for flag, handler in filter_handlers.items():
                if flags[flag] is not None:
                    # Update the last element of track_data with the filtered track_info
                    track_data[-1] = handler(track_info, features, flags[flag])
    # Artist search
    else:
        for id in ids:
            results = spotify.artist_top_tracks(artist_id=id, country="US")
            track_ids = [track["id"] for track in results["tracks"]]
            if track_ids:
                all_info = get_track_info_and_features(track_ids)  # gets track info and features
                # for all requested info
                for track_info, features in all_info:
                    # Operation is always done
                    track_data.append(track_info)
                    # Apply filters
                    for flag, handler in filter_handlers.items():
                        if flags[flag] is not None:
                            track_data[-1] = handler(track_info, features, flags[flag])
    df = create_dataframe(track_data)

    return df
