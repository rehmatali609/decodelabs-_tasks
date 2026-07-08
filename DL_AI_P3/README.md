# 🎯 AI Recommendation Engine

A production-style **Content-Based Recommendation System** built with Python that provides personalized course recommendations based on user preferences. The engine evaluates multiple attributes including category, difficulty level, budget, interests, keywords, popularity, ratings, and student enrollment to recommend the most relevant courses with explainable similarity scores.

This project was developed as **Project 3** during my **AI Internship at DecodeLabs**.

---

## 🚀 Features

- 🤖 Personalized course recommendations
- 🎯 Content-based recommendation algorithm
- 📊 Weighted similarity scoring
- 🔍 Keyword-based course search
- 🏷️ Interest and tag matching
- ⭐ Minimum rating filter
- 💰 Budget preference matching
- 📈 Popularity-based ranking
- 📚 Student enrollment consideration
- 📋 Recommendation confidence levels
- 📑 Score breakdown for explainable AI
- 💬 User feedback collection (1–5 stars)
- 📝 Recommendation history tracking
- 💾 Persistent history storage (JSON)
- 🛡️ Input validation and exception handling
- 🏗️ Modular and production-ready architecture

---

# 🏗️ System Architecture

```text
                 User Preferences
                        │
                        ▼
               Input Collection Module
                        │
                        ▼
              Input Normalization Module
                        │
                        ▼
         Content-Based Recommendation Engine
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
 Category Match   Keyword Match   Tag Matching
         ▼              ▼              ▼
      Rating Filter  Budget Match  Popularity
         └──────────────┼──────────────┘
                        ▼
          Similarity Score Calculation
                        ▼
              Recommendation Ranking
                        ▼
          Confidence & Score Breakdown
                        ▼
           Top Course Recommendations
                        ▼
          User Feedback & History Storage
```

---

# 📂 Project Structure

```text
AI-Recommendation-Engine/
│
├── data/
│   └── courses.json
│
├── history.json
├── main.py
├── recommendation_engine.py
├── similarity.py
├── history.py
├── utils.py
├── requirements.txt
└── README.md
```

---

# 🛠️ Technologies Used

- Python 3
- JSON
- Content-Based Filtering
- Weighted Similarity Algorithm
- Modular Programming

---

# ⚙️ How It Works

The recommendation engine collects the following user preferences:

- Favorite Category
- Preferred Difficulty
- Budget
- Interests / Tags
- Search Keywords
- Minimum Course Rating

The engine compares these preferences with the available course dataset and computes a weighted similarity score for each course.

Recommendations are ranked based on:

- Category Match
- Difficulty Match
- Budget Match
- Interest Match
- Keyword Match
- Popularity Score
- Course Rating
- Student Enrollment

The system then displays:

- Similarity Score
- Recommendation Confidence
- Score Breakdown
- Reasons for Recommendation

---

# 📊 Example Output

```text
=========================================
AI Recommendation Engine
=========================================

Favorite Category: AI
Preferred Difficulty: Beginner
Preferred Budget: Free
Favorite Tags: Programming
Search Keywords: Python
Minimum Rating: 4.5

Top Recommendations

1. Python for AI

Category: AI
Difficulty: Beginner
Price: Free

Similarity Score: 92.45%
Confidence: High

Score Breakdown

- Category Match: 30%
- Budget Match: 20%
- Keyword Match: 15%
- Interest Match: 10%
- Rating Bonus: 10%
- Popularity Bonus: 7%
- Student Interest: 5%

Why it matches

- Category Match
- Budget Match
- Keyword Match
- High Rating
- Popularity Bonus
```

---

# 📈 Recommendation Workflow

1. Collect user preferences
2. Normalize user input
3. Load course dataset
4. Compare user preferences with course attributes
5. Calculate weighted similarity scores
6. Rank all courses
7. Display top recommendations
8. Collect user feedback
9. Save recommendation history

---

# 📚 Recommendation Factors

The recommendation engine evaluates:

- 📂 Course Category
- 📖 Difficulty Level
- 💰 Price/Budget
- 🏷️ User Interests
- 🔍 Search Keywords
- ⭐ Course Rating
- 📈 Popularity Score
- 👨‍🎓 Student Enrollment

Each factor contributes to the overall similarity score.

---

# 📝 Recommendation History

Each recommendation session is automatically saved.

Stored information includes:

- Timestamp
- User Preferences
- Top 3 Recommended Courses
- Similarity Scores
- User Feedback

Users can review previous recommendation sessions directly from the application.

---

# 💡 Explainable AI

Unlike basic recommendation systems, this project explains *why* each recommendation was selected.

For every recommended course, the system displays:

- Similarity Score
- Confidence Level
- Score Breakdown
- Matching Reasons

This improves transparency and user trust.

---

# ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/AI-Recommendation-Engine.git
```

Navigate to the project directory:

```bash
cd AI-Recommendation-Engine
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Project

```bash
python main.py
```

---

# 🎯 Learning Outcomes

This project demonstrates:

- Recommendation Systems
- Content-Based Filtering
- Similarity Scoring
- Explainable AI (XAI)
- User Preference Analysis
- Ranking Algorithms
- JSON Data Processing
- Persistent Storage
- Exception Handling
- Modular Python Development

---

# 🔮 Future Improvements

- Collaborative Filtering
- Hybrid Recommendation System
- Machine Learning-based Recommendations
- User Authentication
- Personalized User Profiles
- SQLite/MySQL Database Support
- REST API Integration
- Streamlit or Flask Web Dashboard
- Recommendation Analytics
- Continuous Learning from User Feedback

---

# 👨‍💻 Author

**Rehmat Ali**

**AI Intern | Computer Engineering Student**

GitHub: https://github.com/rehmatali609

LinkedIn: https://www.linkedin.com/in/rehmat-ali-49a09932b

---

# 📄 License

This project was developed for educational purposes as part of the **DecodeLabs Artificial Intelligence Internship Program**.
