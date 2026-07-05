import os
import json
from datetime import datetime

def ensure_folder(path):
    if not path:
        return
    folder = path
    if os.path.splitext(path)[1]:
        folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)


def save_json(path, data):
    ensure_folder(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_text(path, text):
    ensure_folder(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def format_duration(seconds):
    return f"{seconds:.2f} sec"


def timestamped_filename(prefix, ext):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{ext}"
