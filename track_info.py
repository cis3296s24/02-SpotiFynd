#track_info is responsible for getting track information and features from the Spotify API
#it is used in main.py to get the track information and features for the top_tracks command
#as well as handle the API key bypass or input
from pkce import spotify


#Retrieves track information and features from the Spotify API
def get_track_info_and_features(ids: list):
    all_info = [] #list of both track info and features

    # Split ids into batches of 100
    id_batches = [ids[i:i + 100] for i in range(0, len(ids), 100)]

    for id_batch in id_batches:
        results = spotify.tracks(id_batch) #for artist, song, album
        features = spotify.audio_features(id_batch) #for tempo, pitch, etc

        for i, track in enumerate(results["tracks"]):
            track_info = {
                "Art": track["album"]["images"][0]["url"],
                "Artists": ", ".join(artist["name"] for artist in track["artists"]),
                "Song": track["name"],
                "uri": track["uri"],
            }
            all_info.append((track_info, features[i])) #appends track info and features to all_info

    return all_info