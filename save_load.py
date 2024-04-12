#save_load.py is responsible for saving and loading filters to and from a JSON file. It is used in main.py to save and load filters for the top_tracks command.
import os
import json

def save_filters(pitch, tempo, danceability, time_signature, acousticness):
    saved_filters = {}
    if pitch is not None:
        saved_filters["pitch"] = pitch
    if tempo is not None:
        saved_filters["tempo"] = tempo
    if danceability is not None:
        saved_filters["danceability"] = danceability
    if time_signature is not None:
        saved_filters["time_signature"] = time_signature
    if acousticness is not None:
        saved_filters["acousticness"] = acousticness
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(saved_filters, file, ensure_ascii=False, indent=4)

def load_filters():
    if not os.path.exists("data.json"):
        raise ValueError("No saved filter. Create one with --save")
    with open("data.json", "r") as file:
        data = json.load(file)

        pitch = data.get("pitch")
        tempo = data.get("tempo")
        danceability = data.get("danceability")
        time_signature = data.get("time_signature")
        acousticness = data.get("acousticness")
    return pitch, tempo, danceability, time_signature, acousticness