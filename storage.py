import os
import json

APP_NAME = "AutoCleanScheduler"

def get_data_path():
    # Documents folder
    documents = os.path.join(os.path.expanduser("~"), "Documents")
    # App folder directly in Documents
    app_folder = os.path.join(documents, APP_NAME)
    os.makedirs(app_folder, exist_ok=True)  # create if not exists
    
    # JSON file directly inside the app folder
    return os.path.join(app_folder, "schedules.json")

DATA_FILE = get_data_path()

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"settings": {"theme": "light"}, "folders": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
