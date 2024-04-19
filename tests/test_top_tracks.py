import pytest
from top_tracks import get_top_tracks
import pandas as pd

def test_get_top_tracks_artist():
    #Checks top tracks for The Wonder Years
    df = get_top_tracks(artist='The Wonder Years', song=None, pitch=None, tempo=None, danceability=None, time_signature=None, acousticness=None, liveness=None, energy=None, speechiness=None, help=None, save=None, load=None)
    #Check df has results
    assert not df.empty
    #Check output artists match input
    assert df['Artist'].str.contains('The Wonder Years').any()

def test_get_top_tracks_song():
    #Checks top tracks for Came Out Swinging
    df = get_top_tracks(song='Came Out Swinging', artist=None, pitch=None, tempo=None, danceability=None, time_signature=None, acousticness=None, liveness=None, energy=None, speechiness=None, help=None, save=None, load=None)
    #Check df has results
    assert not df.empty
    #Check that output song names contains the input song
    assert df['Song'].str.contains('Came Out Swinging').any()