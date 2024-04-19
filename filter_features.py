#filter_features.py contains all of the filtering functions used by top_tracks in main.py.
#When adding a new filter, you must add it in main.py to:
#1. filter_handlers dictionary in utility.py
#2. potential arguments in the top_tracks function in top_tracks.py
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

#For filtering acousticness
def filter_acousticness(track_info, features, acousticness):
    min_acoust, max_acoust = map(float, acousticness.split('-'))
    #Check to make sure acousticness is given within range 0-1
    if min_acoust < 0.0 or max_acoust > 1.0:
        raise ValueError(f"Acousticness outside scope. Values must be between 0.0 and 1. Ex: 0.3-0.7")
    if min_acoust <= features["acousticness"] <= max_acoust:
        track_info["Acousticness"] = features["acousticness"]
    return track_info

#For filtering time signature enter a value between 3 and 7 representing that number/4 ex: "3" -> 3/4 time
def filter_time_signature(track_info, features, time_signature):
    if int(time_signature) < 3 or int(time_signature) > 7:
        raise ValueError(f"Time Signature outside scope. Values must be between 3 and 7")
    if features["time_signature"] == int(time_signature):
        track_info["Time Signature"] = features["time_signature"]
    return track_info

#For filtering liveness
def filter_liveness(track_info, features, liveness):
    min_live, max_live = map(float, liveness.split('-'))
    #Check to make sure liveness is given within range 0-1
    if min_live < 0.0 or max_live > 1.0:
        raise ValueError(f"Liveness outside scope. Values must be between 0.0 and 1. Ex: 0.1-0.9")
    if min_live <= features["liveness"] <= max_live:
        track_info["Liveness"] = features["liveness"]
    return track_info

#For filtering energy
def filter_energy(track_info, features, energy):
    min_energy, max_energy = map(float, energy.split('-'))
    #Check to make sure energy is within given range 0-1
    if min_energy < 0.0 or max_energy > 1.0:
        raise ValueError(f"Energy outside scope. Values must be between 0.0 and 1.0. Ex: 0.2-0.8")
    if min_energy <= features["energy"] <= max_energy:
        track_info["Energy"] = features["energy"]
    return track_info

#For filtering song speechiness
def filter_speechiness(track_info, features, speechiness):
    min_speechiness, max_speechiness = map(float, speechiness.split('-'))
    #Check to make sure speechiness is within given range 0-1
    if min_speechiness < 0.0 or max_speechiness > 1.0:
        raise ValueError(f"Speechiness outside scope. Values must be between 0.0 and 1.0. Ex: 0.2-0.8")
    if min_speechiness <= features["speechiness"] <= max_speechiness:
        track_info["Speechiness"] = features["speechiness"]
    return track_info 

