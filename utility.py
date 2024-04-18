
from filter_features import filter_pitch, filter_tempo, filter_danceability, filter_acousticness, filter_time_signature, filter_liveness, filter_energy
from track_info import spotify

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