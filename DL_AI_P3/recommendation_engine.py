import random
from dataclasses import asdict
from typing import Dict, List, Tuple, Union

try:
    from .dataset import Course, load_courses
    from .utils import normalize_input, normalize_text
except ImportError:
    from dataset import Course, load_courses
    from utils import normalize_input, normalize_text


WEIGHTS = {
    "category": 25,
    "difficulty": 18,
    "budget": 12,
    "keyword": 12,
    "tag": 8,
    "popularity": 10,
    "students": 7,
    "rating": 8,
}

MAX_STUDENT_SCALE = 15000
MAX_SCORE = 100.0


def _get_value(source: Union[Dict[str, object], Course], key: str, default="") -> object:
    if isinstance(source, dict):
        return source.get(key, default)
    return getattr(source, key, default)


def _normalize_tags(value: Union[str, List[str]]) -> set:
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    return set(normalize_input(str(value)))


def _extract_keywords(user: Dict[str, object]) -> set:
    keywords = user.get("keywords", [])
    if isinstance(keywords, str):
        keywords = normalize_input(keywords)
    return set(keywords)


def _get_confidence_label(score: float) -> str:
    if score >= 75:
        return "Excellent Match"
    if score >= 55:
        return "Good Match"
    if score >= 35:
        return "Fair Match"
    return "Low Match"


def calculate_similarity(user: Dict[str, object], course: Union[Dict[str, object], Course]) -> Tuple[float, List[str], List[Tuple[str, float]], str]:
    reasons: List[str] = []
    breakdown: List[Tuple[str, float]] = []
    score = 0.0
    base_score = 0.0

    user_category = normalize_text(user.get("category", ""))
    course_category = normalize_text(_get_value(course, "category", ""))
    if user_category and user_category == course_category:
        score += WEIGHTS["category"]
        reasons.append("Category Match")
        breakdown.append(("Category Match", WEIGHTS["category"]))

    user_difficulty = normalize_text(user.get("difficulty", ""))
    course_difficulty = normalize_text(_get_value(course, "difficulty", ""))
    if user_difficulty and user_difficulty == course_difficulty:
        score += WEIGHTS["difficulty"]
        reasons.append("Difficulty Match")
        breakdown.append(("Difficulty Match", WEIGHTS["difficulty"]))

    user_budget = normalize_text(user.get("budget", ""))
    course_price = normalize_text(_get_value(course, "price", ""))
    if user_budget and user_budget == course_price:
        score += WEIGHTS["budget"]
        reasons.append("Budget Match")
        breakdown.append(("Budget Match", WEIGHTS["budget"]))

    user_tags = _normalize_tags(user.get("tags", []))
    course_tags = _normalize_tags(_get_value(course, "tags", []))
    matched_tags = sorted(user_tags & course_tags)
    for tag in matched_tags:
        score += WEIGHTS["tag"]
        reasons.append(f"Tag Match: {tag.title()}")
        breakdown.append((f"Tag: {tag.title()}", WEIGHTS["tag"]))

    user_keywords = _extract_keywords(user)
    if user_keywords:
        course_text = f"{_get_value(course, 'name', '')} {' '.join(_get_value(course, 'tags', []))}"
        normalized_course_text = normalize_text(course_text)
        matched_keywords = [keyword for keyword in user_keywords if keyword in normalized_course_text]
        if matched_keywords:
            score += WEIGHTS["keyword"]
            reasons.append(f"Keyword Match: {matched_keywords[0].title()}")
            breakdown.append(("Keyword Match", WEIGHTS["keyword"]))

    base_score = score

    popularity = float(_get_value(course, "popularity", 0.0))
    popularity_bonus = (popularity / 5.0) * WEIGHTS["popularity"]
    score += popularity_bonus
    if popularity > 0:
        reasons.append("Popularity Bonus")
        breakdown.append(("Popularity Bonus", round(popularity_bonus, 2)))

    students = int(_get_value(course, "students", 0) or 0)
    if students > 0:
        students_bonus = min(students / MAX_STUDENT_SCALE, 1.0) * WEIGHTS["students"]
        score += students_bonus
        reasons.append("Student Interest")
        breakdown.append(("Student Interest", round(students_bonus, 2)))

    rating_preference = float(user.get("minimum_rating", 0) or 0)
    course_rating = float(_get_value(course, "rating", 0.0) or 0.0)
    if rating_preference > 0:
        if course_rating >= rating_preference:
            score += WEIGHTS["rating"]
            reasons.append("Rating Preference Met")
            breakdown.append(("Rating Bonus", WEIGHTS["rating"]))
        else:
            reasons.append("Below Preferred Rating")

    similarity = round(min(score, MAX_SCORE), 2)
    confidence = _get_confidence_label(similarity)
    return similarity if base_score > 0 else 0.0, reasons, breakdown if base_score > 0 else [], confidence


def rank_courses(user: Dict[str, object], courses: List[Union[Dict[str, object], Course]]) -> List[Dict[str, object]]:
    scored_courses = []
    for course in courses:
        score, reasons, breakdown, confidence = calculate_similarity(user, course)
        course_data = asdict(course) if hasattr(course, "__dataclass_fields__") else dict(course)
        course_data.update(
            {
                "similarity_score": score,
                "reasons": reasons,
                "breakdown": breakdown,
                "confidence": confidence,
            }
        )
        scored_courses.append(course_data)

    ranked = sorted(
        scored_courses,
        key=lambda item: (-item["similarity_score"], -item.get("popularity", 0.0), random.random()),
    )
    return ranked


def get_top_recommendations(user: Dict[str, object], top_n: int = 3) -> List[Dict[str, object]]:
    courses = load_courses()
    ranked = rank_courses(user, courses)
    if not ranked:
        return []

    if all(item["similarity_score"] == 0 for item in ranked):
        popular = sorted(
            ranked,
            key=lambda item: (-item.get("popularity", 0.0), -item.get("students", 0), random.random()),
        )
        return [
            {
                **item,
                "similarity_score": 0.0,
                "reasons": ["Cold Start Popular Recommendation"],
                "breakdown": [("Cold Start Popular Recommendation", 0.0)],
                "confidence": "★★ Low Match",
            }
            for item in popular[:top_n]
        ]

    return ranked[:top_n]
