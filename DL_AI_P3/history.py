import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

HISTORY_FILE = Path(__file__).resolve().parent / "recommendation_history.json"


def _ensure_history_file() -> None:
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text(json.dumps([]), encoding="utf-8")


def load_history() -> List[Dict[str, Any]]:
    _ensure_history_file()
    try:
        payload = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(payload, list):
        return []
    return payload


def save_history(user: Dict[str, Any], recommendations: List[Dict[str, Any]], feedback: Any = None) -> None:
    history = load_history()
    entry = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "user": {
            "category": user.get("category", ""),
            "difficulty": user.get("difficulty", ""),
            "budget": user.get("budget", ""),
            "tags": user.get("tags", []),
            "minimum_rating": user.get("minimum_rating", 0.0),
        },
        "recommendations": [
            {
                "name": rec.get("name", ""),
                "similarity_score": rec.get("similarity_score", 0.0),
                "reasons": rec.get("reasons", []),
            }
            for rec in recommendations
        ],
        "feedback": feedback,
    }
    history.insert(0, entry)
    HISTORY_FILE.write_text(json.dumps(history[:20], indent=2), encoding="utf-8")
