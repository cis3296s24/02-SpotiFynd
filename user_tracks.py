import collections
from pkce import spotify
from dataframe import create_dataframe

pitch_names = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

def generate_user_tracks(limit=50):
    #Retrieve the user's saved tracks
    saved_tracks = spotify.current_user_saved_tracks()
    saved_track_ids = set(track['track']['id'] for track in saved_tracks['items'])

    #Retrieve the user's top tracks up to 100 songs
    top_tracks = spotify.current_user_top_tracks(time_range='medium_term', limit=min(limit, 50))

    #Get the artist IDs from the top tracks
    artist_ids = [track['artists'][0]['id'] for track in top_tracks['items']]

    #Get information about all user saved artists
    artists = spotify.artists(artist_ids)

    #Get the genres of their artists
    top_artist_genres = [artist['genres'] for artist in artists['artists']]

    #Get the song IDs
    top_track_ids = [track['id'] for track in top_tracks['items']]

    #Find the most common genres. The amount for this + seeded tracks must = 5
    flattened_genres = [genre for genres in top_artist_genres for genre in genres]
    #(number) + seeded_tracks cannot exceed 5
    most_common_genre = collections.Counter(flattened_genres).most_common(1)[0][0] 

    #Combine seeds for song recommendations [:#] value corresponds to weight. These values + most_common_genre cannot exceed 5
    seeded_tracks = (list(saved_track_ids)[:2] + top_track_ids[:2])

    #Retrieve song recommendations based on track and genre seeds
    song_recommendations = spotify.recommendations(seed_tracks=seeded_tracks, seed_genres=[most_common_genre], limit=limit)

    #Prepare the data for create_dataframe
    track_data = []
    recommended_track_ids = [track['id'] for track in song_recommendations['tracks'] if track['id'] not in saved_track_ids]
    #Get all features in one API call
    track_audio_features_list = spotify.audio_features(recommended_track_ids)

    for track, track_audio_features in zip(song_recommendations['tracks'], track_audio_features_list):
        #Skip the song if already saved
        if track['id'] in saved_track_ids:
            continue
        #Else add it to be output to dataframe
        track_info = {
            "Art": track["album"]["images"][0]["url"],
            "Artist": track["artists"][0]["name"],
            "Song": track["name"],
            "Key": pitch_names[track_audio_features['key']] if track_audio_features['key'] is not None else None,
        }
        for audio_feature in track_audio_features:
            if audio_feature not in ['type', 'id', 'track_href', 'analysis_url', 'key']:
                track_info[audio_feature] = track_audio_features[audio_feature]
        track_data.append(track_info)

    #Create a dataframe from the song recommendations
    df = create_dataframe(track_data)

    return df