#used to test save_load.py
import os
import json
from save_load import save_filters, load_filters

def test_save_and_load_filters():
    #set filters to be saved
    import os
import json
from save_load import save_filters, load_filters

def test_save_and_load_filters():
    pitch = "0-1"
    tempo = "100-200"
    danceability = "0.7-0.9"
    time_signature = "3-4"
    acousticness = "0.1-0.3"
    energy = "0.8-1.0"

    #Save the filters with the above values
    save_filters(pitch, tempo, danceability, time_signature, acousticness, energy)

    #Set filters to be saved
    save_filters(pitch, tempo, danceability, time_signature, acousticness, energy)

    #Load the filters saved above
    loaded_pitch, loaded_tempo, loaded_danceability, loaded_time_signature, loaded_acousticness, loaded_energy = load_filters()

    #Check that loaded and saved values are the same
    assert pitch == loaded_pitch
    assert tempo == loaded_tempo
    assert danceability == loaded_danceability
    assert time_signature == loaded_time_signature
    assert acousticness == loaded_acousticness
    assert energy == loaded_energy

    #Remove the testing file
    os.remove("data.json")