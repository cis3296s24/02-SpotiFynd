#filter_features.py contains all of the filtering functions used by top_tracks in main.py.
#When adding a new filter, you must add it in main.py to:
#1. filter_handlers dictionary above top_tracks
#2. potential arguments in the top_tracks function
#3. flags passed section (elif song or tempo or ...) in top_tracks
#4. flags dictionary in top_tracks

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


#For filtering time signature enter a value between 3 and 7 representing that number/4 ex: "3" -> 3/4 time
def filter_time_signature(track_info, features, time_signature):
    if int(time_signature) < 3 or int(time_signature) > 7:
        raise ValueError(f"Time Signature outside scope. Values must be between 3 and 7")
    if features["time_signature"] == int(time_signature):
        track_info["Time Signature"] = features["time_signature"]
    return track_info
        
#For filtering acousticness
def filter_acousticness(track_info, features, acousticness):
    min_acoust, max_acoust = map(float, acousticness.split('-'))
    #Check to make sure acousticness is given within range 0-1
    if min_acoust < 0.0 or max_acoust > 1.0:
        raise ValueError(f"Acousticness outside scope. Values must be between 0.0 and 1. Ex: 0.3-0.7")
    if min_acoust <= features["acousticness"] <= max_acoust:
        track_info["Acousticness"] = features["acousticness"]
    return track_info