import json
import os

BASE_DIR = "data/database"

def load_json(fn, default):
    """
    Load a JSON file and return its content. If the file does not exist, return the default value.

    Args:
        fn (str): The filename of the JSON file.
        default (any): The default value to return if the file does not exist.

    Returns:
        any: The content of the JSON file or the default value.
    """
    p = os.path.join(BASE_DIR, fn)
    if not os.path.exists(p):
        return default
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {p}")
        return default
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return default

def save_json(fn, data):
    """
    Save data to a JSON file.

    Args:
        fn (str): The filename of the JSON file.
        data (any): The data to save in JSON format.
    """
    os.makedirs(BASE_DIR, exist_ok=True)  # Ensure the base directory exists
    p = os.path.join(BASE_DIR, fn)
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
