# save_load.py is responsible for saving and loading filters to and from a JSON file. It is used in main.py to save and load filters for the top_tracks command.
import json
import os

DATA_FILE = "data.json"


def save_filters(**kwargs):
    saved_filters = {k: v for k, v in kwargs.items() if v is not None}
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(saved_filters, file, ensure_ascii=False, indent=4)


def load_filters():
    if not os.path.exists(DATA_FILE):
        raise ValueError("No saved filter. Create one with --save.")
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
