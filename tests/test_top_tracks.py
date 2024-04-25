import pytest
from main import top_tracks

def test_top_tracks():
    #Checks top tracks for The Wonder Years
    df = top_tracks('The Wonder Years',
                    save=False,
                    load=False,
                    acousticness=None,
                    danceability=None,
                    duration_ms=None,
                    energy=None,
                    instrumentalness=None,
                    key=None,
                    liveness=None,
                    loudness=None,
                    mode=None,
                    popularity=None,
                    speechiness=None,
                    tempo=None,
                    time_signature=None,
                    valence=None)
    assert len(df) == 10
    assert "The Wonder Years" in df["Artists"].values

