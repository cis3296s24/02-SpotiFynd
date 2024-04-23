from typer import Option
from filter_features import filter_pitch, filter_tempo, filter_danceability, filter_acousticness, filter_time_signature, filter_liveness, filter_energy, filter_speechiness
from pkce import spotify

def uri_from_search(name: str, search_type: str):
    #limit determines amount of results, artist and album are limited to 10 results via API
    results = spotify.search(q=f"{search_type}:" + name, type=search_type, limit=50)
    items = results[search_type + "s"]["items"]
    #prints the amount of results
    if len(items) > 0:
        return [item["id"] for item in items]
    else:
        raise ValueError(f"No {search_type}s found with the name {name}")


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

    return Option(None, short_flag, long_flag, help=f"{minimum} to {maximum}", parser=number_range)


def artists_from_string(string: str) -> list[str]:
    return [uri_from_search(artist.strip(), "artist")[0] for artist in string.split(",")]


def tracks_from_string(string: str) -> list[str]:
    return [uri_from_search(track.strip(), "track")[0] for track in string.split(",")]


def genres_from_string(string: str) -> list[str]:
    return [genre.strip() for genre in string.split(",")]

#Dictionary of filter handlers for filtering in top_tracks, this is used when filtering a song by feature

filter_handlers = {"pitch": filter_pitch, "tempo": filter_tempo, "danceability": filter_danceability,"acousticness": filter_acousticness, "time_signature": filter_time_signature, "liveness": filter_liveness, "energy": filter_energy, "speechiness": filter_speechiness}