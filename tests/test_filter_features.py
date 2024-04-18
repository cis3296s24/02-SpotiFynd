#used to test filter_features.py
import pytest
from filter_features import filter_pitch, filter_tempo, filter_danceability, filter_acousticness, filter_time_signature, filter_liveness, filter_energy

#Tests will set the features of a song and then filter the song based on the feature
def test_filter_pitch():
    track_info = {}
    features = {"key": 5}
    pitch = "5"
    result = filter_pitch(track_info, features, pitch)
    assert result["Pitch"] == "F"

def test_filter_tempo():
    track_info = {}
    features = {"tempo": 120.0}
    tempo = "100-200"
    result = filter_tempo(track_info, features, tempo)
    assert result["Tempo"] == 120.0

def test_filter_danceability():
    track_info = {}
    features = {"danceability": 0.5}
    danceability = "0.1-0.9"
    result = filter_danceability(track_info, features, danceability)
    assert result["Danceability"] == 0.5

def test_filter_acousticness():
    track_info = {}
    features = {"acousticness": 0.5}
    acousticness = "0.1-0.9"
    result = filter_acousticness(track_info, features, acousticness)
    assert result["Acousticness"] == 0.5

def test_filter_time_signature():
    track_info = {}
    features = {"time_signature": 4}
    time_signature = "4"
    result = filter_time_signature(track_info, features, time_signature)
    assert result["Time Signature"] == 4

def test_filter_liveness():
    track_info = {}
    features = {"liveness": 0.5}
    liveness = "0.1-0.9"
    result = filter_liveness(track_info, features, liveness)
    assert result["Liveness"] == 0.5

def test_filter_energy():
    track_info = {}
    features = {"energy": 0.5}
    energy = "0.1-0.9"
    result = filter_energy(track_info, features, energy)
    assert result["Energy"] == 0.5