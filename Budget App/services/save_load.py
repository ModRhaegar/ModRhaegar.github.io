import json
import os

DATA_FILE = "data/data.json"

def save_data(manager):
    with open(DATA_FILE, "w") as f:
        json.dump(manager.to_dict(), f, indent=4)

def load_data(manager):
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        manager.load_from_dict(data)