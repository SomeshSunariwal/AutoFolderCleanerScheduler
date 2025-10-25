# storage.py
import os, json, ctypes

APP_NAME = "AutoCleanScheduler"

def get_data_path():
    documents = os.path.join(os.path.expanduser("~"), "Documents")
    app_folder = os.path.join(documents, APP_NAME, "data")
    os.makedirs(app_folder, exist_ok=True)
    # hide folder
    try:
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(app_folder, FILE_ATTRIBUTE_HIDDEN)
    except Exception:
        pass
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
