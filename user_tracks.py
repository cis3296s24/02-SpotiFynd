import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
from dataframe import create_dataframe

def generate_user_tracks():

    #Create a Spotify object with the user's credentials
    user_spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-library-read'))

    #Retrieve the user's saved tracks
    results = user_spotify.current_user_saved_tracks()

    #Get the audio features for each of the user's saved tracks
    tracks = results['items']
    track_ids = [track['track']['id'] for track in tracks]
    features = user_spotify.audio_features(track_ids)

    #Calculate the average values for each feature
    avg_features = {feature: np.mean([f[feature] for f in features]) for feature in features[0]}

    #median features
    median_features = {feature: np.median([f[feature] for f in features]) for feature in features[0]}

    #perhaps maybe find another way to do this aside from the mean???

    #Get recommendations based on the average features, need to modify to allow user to choose type
    song_recommendations = user_spotify.recommendations(seed_genres=[], target_audio_features=median_features)

    df = create_dataframe(song_recommendations)