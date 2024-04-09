#track_info is responsible for getting track information and features from the Spotify API
#it is used in main.py to get the track information and features for the top_tracks command
#as well as handle the API key bypass or input
import spotipy
import skip_auth
spotify = spotipy.Spotify(auth=skip_auth.access_token()) 

#Retrieves track information and features from the Spotify API
def get_track_info_and_features(ids: list):
    results = spotify.tracks(ids) #for artist, song, album
    features = spotify.audio_features(ids) #for tempo, pitch, etc
    all_info = [] #list of both track info and features

    for i, track in enumerate(results["tracks"]):
        track_info = {
            "Art": track["album"]["images"][0]["url"],
            "Artist": track["artists"][0]["name"], 
            "Song": track["name"],
        }
        all_info.append((track_info, features[i])) #appends track info and features to all_info

    return all_info