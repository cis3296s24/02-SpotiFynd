import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
import collections
from dataframe import create_dataframe
from credentials import cred

#By default suggestions are limited to 50 songs
def generate_user_tracks(limit=50):

    #Create a Spotify object with the user's credentials
    user_spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret, redirect_uri=cred.redirect_uri, scope=cred.scope))

    #Retrieve the user's saved tracks
    results = user_spotify.current_user_saved_tracks()

    #Get the audio features and genres for each of the user's saved tracks
    tracks = results['items']
    track_ids = [track['track']['id'] for track in tracks]
    features = user_spotify.audio_features(track_ids)
    genres = [user_spotify.artist(track['track']['artists'][0]['id'])['genres'] for track in tracks]

    #Weight the seeding by the top genres
    genres = [genre for sublist in genres for genre in sublist]
    top_genres = [genre for genre, count in collections.Counter(genres).most_common(5)]

    #Calculate the average values for each feature
    avg_features = {feature: np.mean([f[feature] for f in features]) for feature in features[0]}

    #Get recommendations based on the top genres and average features
    song_recommendations = user_spotify.recommendations(seed_genres=top_genres, limit=limit)