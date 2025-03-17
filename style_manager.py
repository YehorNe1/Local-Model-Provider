# style_manager.py
import os
import json

STYLE_FILE = "style_prefs.json"

def ensure_style_file():
    if not os.path.exists(STYLE_FILE):
        with open(STYLE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

def load_style_prefs() -> dict:
    ensure_style_file()
    try:
        with open(STYLE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_style_prefs(prefs: dict):
    ensure_style_file()
    with open(STYLE_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)