#used to test save_load.py
import os
from save_load import save_filters, load_filters

def test_save_and_load_filters():
    pitch = "0-1"
    tempo = "100-200"
    danceability = "0.7-0.9"
    time_signature = "3-4"
    acousticness = "0.1-0.3"
    energy = "0.8-1.0"

    filters = locals()

    #Save the filters with the above values
    save_filters(**filters)

    #Load the filters saved above
    loaded_filters = load_filters()

    #Check that loaded and saved values are the same
    assert pitch == loaded_filters["pitch"]
    assert tempo == loaded_filters["tempo"]
    assert danceability == loaded_filters["danceability"]
    assert time_signature == loaded_filters["time_signature"]
    assert acousticness == loaded_filters["acousticness"]
    assert energy == loaded_filters["energy"]

    #Remove the testing file
    os.remove("data.json")