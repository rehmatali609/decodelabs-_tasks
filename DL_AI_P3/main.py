from typing import Any, cast, Dict, List, Optional

from recommendation_engine import get_top_recommendations
from utils import normalize_input
try:
    from history import load_history, save_history
except ImportError:
    from .history import load_history, save_history


def prompt_input(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def safe_print(*values: object) -> None:
    try:
        print(*values)
    except UnicodeEncodeError:
        safe_values = [str(value).encode("ascii", errors="replace").decode("ascii") for value in values]
        print(*safe_values)


def collect_user_preferences() -> Dict[str, object]:
    safe_print("=========================================")
    safe_print("AI Recommendation Engine")
    safe_print("=========================================")
    category = prompt_input("Favorite Category: ")
    difficulty = prompt_input("Preferred Difficulty: ")
    budget = prompt_input("Preferred Budget: ")
    tags_input = prompt_input("Favorite Tags/Interests: ")
    keywords_input = prompt_input("Search Keywords (optional): ")
    minimum_rating = prompt_input("Minimum Course Rating (optional, e.g. 4.5): ")

    return {
        "category": category,
        "difficulty": difficulty,
        "budget": budget,
        "tags": normalize_input(tags_input),
        "keywords": normalize_input(keywords_input),
        "minimum_rating": float(minimum_rating) if minimum_rating else 0.0,
    }


def display_results(recommendations: List[Dict[str, object]]) -> None:
    if not recommendations:
        safe_print("\nNo recommendations available at this time. Try broader preferences.")
        return

    safe_print("\nTop Recommendations")
    safe_print("-" * 60)
    for index, course in enumerate(recommendations, start=1):
        safe_print(f"{index}. {course['name']}")
        safe_print(f"   Category: {course['category']} | Difficulty: {course['difficulty']} | Price: {course['price']}")
        safe_print(f"   Popularity: {course.get('popularity', 0.0)} | Rating: {course.get('rating', 0.0)} | Students: {course.get('students', 0)}")
        safe_print(f"   Similarity Score: {course['similarity_score']}%")
        safe_print(f"   Confidence: {course.get('confidence', 'N/A')}")
        breakdown = cast(List[tuple], course.get("breakdown", []))
        if breakdown:
            safe_print("   Score Breakdown:")
            for label, value in breakdown:
                safe_print(f"      - {label}: {value}%")
        reasons = cast(List[str], course.get("reasons", []) or ["Popularity"])
        if reasons:
            safe_print("   Why it matches:")
            for reason in reasons:
                safe_print(f"      - {reason}")
        safe_print("-" * 60)


def collect_feedback(recommendations: List[Dict[str, object]]) -> Optional[int]:
    if not recommendations:
        return None

    top_course = recommendations[0]
    choice = prompt_input(f"Would you like to rate '{top_course['name']}'? (y/n): ").lower()
    if choice != "y":
        return None

    rating_text = prompt_input("Enter rating 1-5 stars: ")
    if rating_text.isdigit() and 1 <= int(rating_text) <= 5:
        return int(rating_text)

    safe_print("Invalid rating. Feedback skipped.")
    return None


def show_history() -> None:
    history = load_history()
    if not history:
        safe_print("\nNo recommendation history found yet.")
        return

    safe_print("\nRecent Recommendation History")
    safe_print("-" * 60)
    for entry in history:
        safe_print(f"Date: {entry['timestamp']}")
        safe_print(f"User: Category={entry['user']['category']} Difficulty={entry['user']['difficulty']} Budget={entry['user']['budget']} Tags={', '.join(entry['user']['tags'])}")
        top_recommendations = [rec.get('name', 'Unknown') for rec in entry.get('recommendations', [])[:3]]
        safe_print("Top 3 Recommendations: ")
        for index, name in enumerate(top_recommendations, start=1):
            safe_print(f"   {index}. {name}")
        if entry.get('feedback') is not None:
            safe_print(f"Feedback: {entry['feedback']} stars")
        safe_print("-" * 60)


def main() -> None:
    while True:
        safe_print("\nChoose an option:")
        safe_print("1. New recommendation")
        safe_print("2. View recommendation history")
        safe_print("3. Exit")
        action = prompt_input("Select 1, 2, or 3: ")

        if action == "2":
            show_history()
            continue
        if action == "3":
            safe_print("Goodbye!")
            break

        user = collect_user_preferences()
        recommendations = get_top_recommendations(user)
        display_results(recommendations)

        feedback = collect_feedback(recommendations)
        save_history(user, recommendations, feedback)

        again = prompt_input("Would you like another recommendation? (1 = Yes, 2 = Exit): ")
        if again == "2":
            break


if __name__ == "__main__":
    main()
