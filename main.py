from typer import Option, Typer
from dataframe import create_dataframe
from utility import artists_from_string, genres_from_string, tracks_from_string, feature
from create_playlist import create_playlist, add_to_playlist
from user_tracks import generate_user_tracks
from top_tracks import get_top_tracks
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

@app.command()
#top_tracks passed arguments based on flags such as -a or -s
def top_tracks(artist: str = Option(None, '-a', '--artist'),
               song: str = Option(None, '-s', '--song'),
               pitch: str = Option(None, '-p', '--pitch'),
               tempo: str = Option(None, '-t', '--tempo'),
               danceability: str = Option(None, '-d', '--dance'),
               time_signature: str = Option(None, '-ts', '--time_signature'),
               acousticness: str = Option(None, '-ac', '--acoustic'),
               liveness: str = Option(None, '-l', '--liveness'),
               energy: str = Option(None, '-e', '--energy'),
               speechiness: str = Option(None, '-sp', '--speechiness'),
               save: bool = None,
               load: bool = None):
    get_top_tracks(artist, song, pitch, tempo, danceability, time_signature, acousticness, liveness, energy, speechiness, save, load)


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
        limit: int = Option(20, "-l", "--limit", help="Number of results to return."),

        artists: str = Option(None, "-a", "--artists", help="Results will be tracks by similar artists.", parser=artists_from_string),
        genres: str = Option(None, "-g", "--genres", help="Results will be in this genre.", parser=genres_from_string),
        tracks: str = Option(None, "-s", "--songs", help="Results will be similar to these tracks.", parser=tracks_from_string),

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
    if artists is None and genres is None and tracks is None:
        raise ValueError("At least one of {artists, genres, tracks} is required.")
    if sum(len(seed) for seed in (artists, genres, tracks) if seed is not None) > 5:
        raise ValueError("The combined total of {artists, genres, tracks} cannot exceed five.")

    searched_features = {k: v for k, v in locals().items() if k not in {"limit", "artists", "genres", "tracks"} and v is not None}
    filters = {}

    for audio_feature, value in searched_features.items():
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

    track_data = []
    for track in results["tracks"]:
        track_info = {
            "Art": track["album"]["images"][0]["url"],
            "Artist": track["artists"][0]["name"],
            "Song": track["name"],
            "uri": track["uri"],
        }
        track_audio_features = spotify.audio_features(track["id"])[0]
        for audio_feature in searched_features:
            source = track if audio_feature == "popularity" else track_audio_features
            track_info[audio_feature] = source[audio_feature]
        track_data.append(track_info)

    create_dataframe(track_data)
    
@app.command()
def suggest(limit: int = Option(50, "-l", "--limit")):
    generate_user_tracks(limit)

@app.command()
def playlist(name: str = Option(None, "-n", "--name")):
    new_playlist = create_playlist(name)
    add_to_playlist(new_playlist)


if __name__ == "__main__":
    app()