import json, os
BASE_DIR = "data/database"
def load_json(fn, default):
    p = os.path.join(BASE_DIR, fn)
    if not os.path.exists(p): return default
    with open(p, "r", encoding="utf-8") as f: return json.load(f)

def save_json(fn, data):
    p = os.path.join(BASE_DIR, fn)
    with open(p, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

