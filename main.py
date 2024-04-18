import typer
from spotipy.oauth2 import SpotifyClientCredentials
from dataframe import create_dataframe
from track_info import spotify
from utility import uri_from_search, filter_handlers
from create_playlist import create_playlist, add_to_playlist
from user_tracks import generate_user_tracks
from top_tracks import get_top_tracks

app = typer.Typer()

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
                   load: bool = None):
    get_top_tracks(artist, song, pitch, tempo, danceability, time_signature, acousticness, liveness, energy, help, save, load)

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
            "uri": track["uri"],
        }
        track_audio_features = spotify.audio_features(track["id"])[0]
        for audio_feature in audio_features:
            track_info[audio_feature] = track_audio_features[audio_feature]
        track_data.append(track_info)

    create_dataframe(track_data)
    
@app.command()
def suggest(limit: int = typer.Option(50, '-l', '--limit')):
    generate_user_tracks(limit)

@app.command()
def playlist(name:str = typer.Option(None, "-n", "--name")):
    new_playlist = create_playlist(name)
    add_to_playlist(new_playlist)

if __name__ == "__main__":
    app()