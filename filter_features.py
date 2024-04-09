#filter_features.py contains all of the filtering functions used by top_tracks in main.py.

#For filtering pitch
#corresponding to 0-11 value for -p search
pitch_names = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

def filter_pitch(track_info, features, pitch):
    if features["key"] == int(pitch):
        track_info["Pitch"] = pitch_names[features["key"]]
    return track_info

#For filtering tempo
def filter_tempo(track_info, features, tempo):
    min_tempo, max_tempo = map(float, tempo.split('-'))
    if min_tempo <= features["tempo"] <= max_tempo:
        track_info["Tempo"] = features["tempo"]
    return track_info

#For filtering danceability
def filter_danceability(track_info, features, danceabillity):
    min_dance, max_dance = map(float, danceabillity.split('-'))
    #checks that the danceability is within the scope of 0-1
    if min_dance < 0.0 or max_dance > 1.0:
        raise ValueError(f"Danceability outside scope. Values must be between 0 and 1")
    if min_dance <= features["danceability"] <= max_dance:
        track_info["Danceability"] = features["danceability"]
    return track_info