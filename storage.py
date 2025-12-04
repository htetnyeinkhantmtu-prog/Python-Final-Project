import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "auth.json")


def load_users():
    if not os.path.exists(DB_PATH):
        return {"users": []}
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save_users(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)
