import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from history import load_history
from recommendation_engine import calculate_similarity, get_top_recommendations, rank_courses
from utils import normalize_input


class RecommendationEngineTests(unittest.TestCase):
    def test_normalize_input_removes_extra_spaces_and_lowercases(self):
        self.assertEqual(normalize_input("  Python   ML  "), ["python", "ml"])

    def test_similarity_scores_category_and_tags(self):
        course = {
            "name": "Python for AI",
            "category": "AI",
            "difficulty": "Beginner",
            "price": "Free",
            "tags": ["python", "ml"],
            "popularity": 4.8,
            "students": 12000,
            "rating": 4.9,
        }
        user = {
            "category": "AI",
            "difficulty": "Beginner",
            "budget": "Free",
            "tags": ["python", "ml"],
        }

        score, reasons, breakdown, confidence = calculate_similarity(user, course)

        self.assertGreater(score, 80)
        self.assertIn("Category Match", reasons)
        self.assertIn("Difficulty Match", reasons)
        self.assertIn("Budget Match", reasons)
        self.assertIn("Tag Match: Python", reasons)
        self.assertIsInstance(breakdown, list)
        self.assertIsInstance(confidence, str)

    def test_rank_courses_returns_best_first(self):
        user = {
            "category": "AI",
            "difficulty": "Beginner",
            "budget": "Free",
            "tags": ["python", "ml"],
        }
        courses = [
            {"name": "Unrelated Course", "category": "Gaming", "difficulty": "Advanced", "price": "Paid", "tags": ["fun"], "popularity": 3.0, "students": 200, "rating": 3.0},
            {"name": "Python for AI", "category": "AI", "difficulty": "Beginner", "price": "Free", "tags": ["python", "ml"], "popularity": 4.8, "students": 12000, "rating": 4.9},
        ]

        ranked = rank_courses(user, courses)
        self.assertEqual(ranked[0]["name"], "Python for AI")

    def test_get_top_recommendations_returns_popular_cold_start(self):
        user = {
            "category": "Sports",
            "difficulty": "Expert",
            "budget": "Luxury",
            "tags": ["surfing"],
            "minimum_rating": 5.0,
        }
        recommendations = get_top_recommendations(user, top_n=2)

        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0]["reasons"], ["Cold Start Popular Recommendation"])

    def test_load_history_returns_empty_for_non_list_json(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            history_file = Path(tmp_dir) / "recommendation_history.json"
            history_file.write_text('{"invalid": true}', encoding="utf-8")

            with patch("history.HISTORY_FILE", history_file):
                self.assertEqual(load_history(), [])


if __name__ == "__main__":
    unittest.main()
