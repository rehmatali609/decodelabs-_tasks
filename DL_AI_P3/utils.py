import re
from typing import List


def normalize_input(value: str) -> List[str]:
    if not value:
        return []

    cleaned = re.sub(r"\s+", " ", value.strip()).lower()
    if "," in cleaned:
        return [item.strip() for item in cleaned.split(",") if item.strip()]

    return [item for item in cleaned.split(" ") if item]


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).lower()
