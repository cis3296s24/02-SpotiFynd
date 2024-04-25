from typer import Option

from pkce import spotify


def uri_from_search(name: str, search_type: str):
    # limit determines amount of results, artist and album are limited to 10 results via API
    results = spotify.search(q=f"{search_type}:{name}", type=search_type, limit=50)
    items = results[f"{search_type}s"]["items"]
    # prints the amount of results
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


def basic_track_info(track: dict) -> dict:
    return {
        "Art": track["album"]["images"][0]["url"],
        "Artists": ", ".join(artist["name"] for artist in track["artists"]),
        "Song": track["name"],
        "uri": track["uri"],
    }


def get_track_info_and_features(ids: list):
    all_info = []  # list of both track info and features

    # Split ids into batches of 100
    id_batches = [ids[i:i + 100] for i in range(0, len(ids), 100)]

    for id_batch in id_batches:
        all_tracks = spotify.tracks(id_batch)["tracks"]  # for artist, song, album
        all_features = spotify.audio_features(id_batch)  # for tempo, pitch, etc

        for track, features in zip(all_tracks, all_features):
            all_info.append((basic_track_info(track), features))  # appends track info and features to all_info

    return all_info


def create_track_data(track_ids: list, audio_features: iter) -> list[dict]:
    track_info_and_features = get_track_info_and_features(track_ids)
    track_data = []
    for track_info, features in track_info_and_features:
        for audio_feature in audio_features:
            source = track_info if audio_features == "popularity" else features
            track_info[audio_feature] = source[audio_feature]
        track_data.append(track_info)
    return track_data
