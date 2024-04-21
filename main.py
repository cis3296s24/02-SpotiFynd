from typer import Option, Typer
from dataframe import create_dataframe
from save_load import load_filters, save_filters
from utility import (
    artists_from_string,
    genres_from_string,
    tracks_from_string,
    feature,
    uri_from_search,
    create_dict
)
from create_playlist import create_playlist, add_to_playlist
from user_tracks import generate_user_tracks
from pkce import spotify

app = Typer()

ACOUSTICNESS = feature("acousticness", 0.0, 1.0)
DANCEABILITY = feature("danceability", 0.0, 1.0)
DURATION_MS = feature("duration_ms", 0, float("inf"))
ENERGY = feature("energy", 0.0, 1.0)
INSTRUMENTALNESS = feature("instrumentalness", 0.0, 1.0)
KEY = feature("key", 0, 11)
LIVENESS = feature("liveness", 0.0, 1.0)
LOUDNESS = feature("loudness", -60.0, 0.0)
MODE = feature("mode", 0, 1)
POPULARITY = feature("popularity", 0, 100)
SPEECHINESS = feature("speechiness", 0.0, 1.0)
TEMPO = feature("tempo", 0.0, float("inf"))
TIME_SIGNATURE = feature("time_signature", 3, 7)
VALENCE = feature("valence", 0.0, 1.0)

SAVE = Option(False, help="Save this set of filters to be used later with --load.")
LOAD = Option(False, help="Load the saved set of filters for this search.")

@app.command()
def top_tracks(
        artist: str,

        save: bool = SAVE,
        load: bool = LOAD,

        acousticness=ACOUSTICNESS,
        danceability=DANCEABILITY,
        duration_ms=DURATION_MS,
        energy=ENERGY,
        instrumentalness=INSTRUMENTALNESS,
        key=KEY,
        liveness=LIVENESS,
        loudness=LOUDNESS,
        mode=MODE,
        popularity=POPULARITY,
        speechiness=SPEECHINESS,
        tempo=TEMPO,
        time_signature=TIME_SIGNATURE,
        valence=VALENCE,
):
    non_audio_features = {"artist", "save", "load", "non_audio_features"}
    searched_audio_features = {k: v for k, v in locals().items() if k not in non_audio_features and v is not None}

    if save:
        save_filters(**searched_audio_features)
    if load:
        searched_audio_features = load_filters()

    artist_id = uri_from_search(artist, "artist")[0]
    tracks = spotify.artist_top_tracks(artist_id)["tracks"]
    track_ids = [track["id"] for track in tracks]
    track_data = create_dict(track_ids, searched_audio_features)

    for audio_feature, value in searched_audio_features.items():
        try:
            low, high = value
        except TypeError:
            raise TypeError("top-tracks only accepts ranges for audio features. See --help for more details.")
        if low is not None:
            track_data = [track for track in track_data if track[audio_feature] >= low]
        if high is not None:
            track_data = [track for track in track_data if track[audio_feature] <= high]

    if not track_data:
        print("No results matching these criteria.")
        return

    df = create_dataframe(track_data)
    return df


@app.command(help="""

Search for tracks based on audio features. Note: at least one of {artists, genres, tracks} is required, and their combined total cannot exceed five. 

For all numerical values, you can provide a range with a dash.

For example, --tempo 100-120 will return tracks with a tempo between 100 and 120.

--valence -0.9 will return tracks with a valence at or below 0.9

--loudness 0.4- will return tracks with a loudness at or above 0.4

For artists, genres, and tracks, you can provide a comma-separated list

For example, -a "artist1, artist2" will return tracks by artists similar to artist1 and artist2.
""")
def similar(
        limit: int = Option(20, "-l", "--limit", help="Number of results to return."),

        artists: str = Option(None, "-a", "--artists", help="Results will be tracks by similar artists.", parser=artists_from_string),
        genres: str = Option(None, "-g", "--genres", help="Results will be in similar genres.", parser=genres_from_string),
        tracks: str = Option(None, "-s", "--songs", help="Results will be similar to these tracks.", parser=tracks_from_string),

        save: bool = SAVE,
        load: bool = LOAD,

        acousticness=ACOUSTICNESS,
        danceability=DANCEABILITY,
        duration_ms=DURATION_MS,
        energy=ENERGY,
        instrumentalness=INSTRUMENTALNESS,
        key=KEY,
        liveness=LIVENESS,
        loudness=LOUDNESS,
        mode=MODE,
        popularity=POPULARITY,
        speechiness=SPEECHINESS,
        tempo=TEMPO,
        time_signature=TIME_SIGNATURE,
        valence=VALENCE,
):
    non_audio_features = {"limit", "artists", "genres", "tracks", "save", "load", "non_audio_features"}
    searched_audio_features = {k: v for k, v in locals().items() if k not in non_audio_features and v is not None}

    if save:
        save_filters(**searched_audio_features)
    if load:
        searched_audio_features = load_filters()

    if artists is None and genres is None and tracks is None:
        raise ValueError("At least one of {artists, genres, tracks} is required.")
    if sum(len(seed) for seed in (artists, genres, tracks) if seed is not None) > 5:
        raise ValueError("The combined total of {artists, genres, tracks} cannot exceed five.")

    filters = {}
    for audio_feature, value in searched_audio_features.items():
        if isinstance(value, tuple):
            low, high = value
            if low is not None:
                filters[f"min_{audio_feature}"] = low
            if high is not None:
                filters[f"max_{audio_feature}"] = high
        else:
            filters[f"target_{audio_feature}"] = value

    results = spotify.recommendations(
        seed_artists=artists,
        seed_genres=genres,
        seed_tracks=tracks,
        limit=limit,
        **filters,
    )

    track_ids = [track["id"] for track in results["tracks"]]
    track_data = create_dict(track_ids, searched_audio_features)

    create_dataframe(track_data)


@app.command()
def suggest(limit: int = 50):
    generate_user_tracks(limit)


@app.command()
def playlist(name: str):
    new_playlist = create_playlist(name)
    add_to_playlist(new_playlist)


if __name__ == "__main__":
    app()
