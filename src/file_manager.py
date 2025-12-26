# hi
# not sure about this file yet
from pathlib import Path
import os
import re
import json
_ILLEGAL = r'[<>:"/\\|?*\x00-\x1F]'
def safe_filename(name: str) -> str:
    if not name:
        return "untitled"
    name = re.sub(_ILLEGAL, "_", name)
    name = name.strip().strip(".")
    return name or "untitled"


def artist_folder_check(artist : str) -> Path:
    base = Path(__file__).resolve().parent.parent / "lyrics"
    sub = base / safe_filename(artist)
    sub.mkdir(parents=True, exist_ok=True)
    return sub

def save_lyrics(artist, track, dictionary):
    sub = artist_folder_check(artist)
    safe_title = (safe_filename(track))
    file_name = f"lyrics_{safe_title}_saved.json"
    lyrics_save_path = sub / file_name
    with open (lyrics_save_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)
    print(f"saved: {lyrics_save_path}")
 