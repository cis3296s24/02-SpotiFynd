import collections
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dataframe import create_dataframe
from credentials import cred

def generate_user_tracks(limit=50):
    #Create a Spotify object with the user's credentials
    user_spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret, redirect_uri=cred.redirect_uri, scope=cred.scope))

    #Retrieve the user's saved tracks
    saved_tracks = user_spotify.current_user_saved_tracks()
    saved_track_ids = [track['track']['id'] for track in saved_tracks['items']]
    
    #Retrieves up to limit amount of users top songs over a period of time
    top_tracks = user_spotify.current_user_top_tracks(time_range='long_term', limit=25)
    top_track_ids = [track['id'] for track in top_tracks['items']]
    
    top_artist_genres = [user_spotify.artist(track['artists'][0]['id'])['genres'] for track in top_tracks['items']]

    #The value amounts for most_common_genres + seeded_tracks must equal 5
    flattened_genres = [genre for genres in top_artist_genres for genre in genres]
    most_common_genres = [genre for genre, _ in collections.Counter(flattened_genres).most_common(1)]
    
    #Combine seeding for song_recommendations
    #The value amounts for most_common_genres + seeded_tracks must equal 5
    seeded_tracks = (saved_track_ids[:3] + top_track_ids[:1])
    
    #Retrieve song recommendations based on seeds
    song_recommendations = user_spotify.recommendations(seed_tracks=seeded_tracks, seed_genres=most_common_genres, limit=limit)

    #Prepare the data for create_dataframe
    track_data = []
    for track in song_recommendations['tracks']:
        #skip the song if already saved
        if track['id'] in saved_track_ids:
            continue
        #else add it to be output to dataframe
        track_info = {
            "Art": track["album"]["images"][0]["url"],
            "Artist": track["artists"][0]["name"],
            "Song": track["name"],
        }
        track_audio_features = user_spotify.audio_features(track["id"])[0]
        for audio_feature in track_audio_features:
            track_info[audio_feature] = track_audio_features[audio_feature]
        track_data.append(track_info)

    #Create a dataframe from the song recommendations
    df = create_dataframe(track_data)

    return df