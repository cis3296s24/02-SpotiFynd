#used for testing the dataframe.py file
import os
import pandas as pd
from dataframe import create_dataframe

def test_create_dataframe():
    #Define track data with known good example values
    track_data = {
        "Art": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
        "Artist": ["Artist1", "Artist2"],
        "Song": ["Song1", "Song2"],
        "Key": ["Key1", "Key2"],
        "uri": ["URI1", "URI2"]
    }

    #Creating this dataframe will also output it to an HTML file per dataframe.py
    df = create_dataframe(track_data)

    #Assert that dataframe has been created with the always defined values.
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["Art", "Artist", "Song", "Key"]
    assert len(df) == 2

    #Check that the HTML file has been created
    assert os.path.exists('df.html')

    #Delete the HTML file
    os.remove('df.html')