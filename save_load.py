#save_load.py is responsible for saving and loading filters to and from a JSON file. It is used in main.py to save and load filters for the top_tracks command.
import os
import json

def save_filters(tempo, pitch):
    saved_filters = {}
    if tempo is not None:
        saved_filters["tempo"] = tempo
    if pitch is not None:
        saved_filters["pitch"] = pitch
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(saved_filters, file, ensure_ascii=False, indent=4)

def load_filters():
    if not os.path.exists("data.json"):
        raise ValueError("No saved filter. Create one with --save")
    with open("data.json", "r") as file:
        data = json.load(file)
        pitch = data.get("pitch")
        tempo = data.get("tempo")
    return pitch, tempo