from typing import Any, cast, Dict, List, Optional

from recommendation_engine import get_top_recommendations
from utils import normalize_input
try:
    from history import load_history, save_history
except ImportError:
    from .history import load_history, save_history


def collect_user_preferences() -> Dict[str, object]:
    print("=========================================")
    print("AI Recommendation Engine")
    print("=========================================")
    category = input("Favorite Category: ").strip()
    difficulty = input("Preferred Difficulty: ").strip()
    budget = input("Preferred Budget: ").strip()
    tags_input = input("Favorite Tags/Interests: ").strip()
    keywords_input = input("Search Keywords (optional): ").strip()
    minimum_rating = input("Minimum Course Rating (optional, e.g. 4.5): ").strip()

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
        print("\nNo recommendations available at this time. Try broader preferences.")
        return

    print("\nTop Recommendations")
    print("-" * 60)
    for index, course in enumerate(recommendations, start=1):
        print(f"{index}. {course['name']}")
        print(f"   Category: {course['category']} | Difficulty: {course['difficulty']} | Price: {course['price']}")
        print(f"   Popularity: {course.get('popularity', 0.0)} | Rating: {course.get('rating', 0.0)} | Students: {course.get('students', 0)}")
        print(f"   Similarity Score: {course['similarity_score']}%")
        print(f"   Confidence: {course.get('confidence', 'N/A')}")
        breakdown = cast(List[tuple], course.get("breakdown", []))
        if breakdown:
            print("   Score Breakdown:")
            for label, value in breakdown:
                print(f"      - {label}: {value}%")
        reasons = cast(List[str], course.get("reasons", []) or ["Popularity"])
        for reason in reasons:
            print(f"   ✓ {reason}")
        print("-" * 60)


def collect_feedback(recommendations: List[Dict[str, object]]) -> Optional[int]:
    if not recommendations:
        return None

    top_course = recommendations[0]
    choice = input(f"Would you like to rate '{top_course['name']}'? (y/n): ").strip().lower()
    if choice != "y":
        return None

    rating_text = input("Enter rating 1-5 stars: ").strip()
    if rating_text.isdigit() and 1 <= int(rating_text) <= 5:
        return int(rating_text)

    print("Invalid rating. Feedback skipped.")
    return None


def show_history() -> None:
    history = load_history()
    if not history:
        print("\nNo recommendation history found yet.")
        return

    print("\nRecent Recommendation History")
    print("-" * 60)
    for entry in history:
        print(f"Date: {entry['timestamp']}")
        print(f"User: Category={entry['user']['category']} Difficulty={entry['user']['difficulty']} Budget={entry['user']['budget']} Tags={', '.join(entry['user']['tags'])}")
        top_recommendations = [rec.get('name', 'Unknown') for rec in entry.get('recommendations', [])[:3]]
        print("Top 3 Recommendations: ")
        for index, name in enumerate(top_recommendations, start=1):
            print(f"   {index}. {name}")
        if entry.get('feedback') is not None:
            print(f"Feedback: {entry['feedback']} stars")
        print("-" * 60)


def main() -> None:
    while True:
        print("\nChoose an option:")
        print("1. New recommendation")
        print("2. View recommendation history")
        print("3. Exit")
        action = input("Select 1, 2, or 3: ").strip()

        if action == "2":
            show_history()
            continue
        if action == "3":
            print("Goodbye!")
            break

        user = collect_user_preferences()
        recommendations = get_top_recommendations(user)
        display_results(recommendations)

        feedback = collect_feedback(recommendations)
        save_history(user, recommendations, feedback)

        again = input("Would you like another recommendation? (1 = Yes, 2 = Exit): ").strip()
        if again == "2":
            break


if __name__ == "__main__":
    main()
