#track_info is responsible for getting track information and features from the Spotify API
#it is used in main.py to get the track information and features for the top_tracks command
#as well as handle the API key bypass or input
from pkce import spotify


#Retrieves track information and features from the Spotify API
def get_track_info_and_features(ids: list):
    all_info = []  # list of both track info and features

    # Split ids into batches of 100
    id_batches = [ids[i:i + 100] for i in range(0, len(ids), 100)]

    for id_batch in id_batches:
        all_tracks = spotify.tracks(id_batch)["tracks"]  # for artist, song, album
        all_features = spotify.audio_features(id_batch)  # for tempo, pitch, etc

        for track, features in zip(all_tracks, all_features):
            track_info = {
                "Art": track["album"]["images"][0]["url"],
                "Artist": track["artists"][0]["name"], 
                "Song": track["name"],
                "URI": track["uri"],
            }
            all_info.append((track_info, features))  # appends track info and features to all_info

    return all_info