#used for testing the user_tracks.py file. Assumes that the credentials.py file is working correctly as is dependent on it.
import pytest
import pandas as pd
from user_tracks import generate_user_tracks

def test_generate_user_tracks():
    # Call the function with a specific limit
    result = generate_user_tracks(limit=10)

    # Check that the result is a DataFrame
    assert isinstance(result, pd.DataFrame)

    # Check that the DataFrame has the expected number of rows
    assert len(result) <= 10

    # Convert column names to lowercase
    result.columns = result.columns.str.lower()

    # Check that the DataFrame has the expected minimum required columns
    expected_columns = ['art', 'artist', 'song', 'danceability', 'energy', 'loudness',
                        'mode', 'speechiness', 'acousticness', 'instrumentalness', 
                        'liveness', 'valence', 'tempo', 'uri', 'duration_ms', 'time_signature']
    print(result.columns)
    assert set(expected_columns).issubset(result.columns)