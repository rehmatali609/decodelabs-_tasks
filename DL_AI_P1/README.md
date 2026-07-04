# 🤖 DecodeLabs AI Chatbot – Hybrid Architecture - Project 1

A Python-based AI chatbot that combines **rule-based intent matching** with a **Large Language Model (LLM) fallback architecture**. The chatbot first attempts deterministic matching for fast and reliable responses. If no suitable response is found, it routes the query to a simulated LLM layer.

This project was developed as part of my AI Internship at DecodeLabs.

---

## 🚀 Features

- Exact intent matching using a response dictionary
- Fuzzy matching for handling typos
- Keyword/substring intent detection
- Simulated LLM fallback for unknown queries
- Randomized responses for natural conversations
- Input sanitization
- Graceful program termination
- Modular and easy-to-extend architecture

---

## 🏗️ Architecture

The chatbot follows a cascading decision pipeline:

User Input
↓
Input Sanitization
↓
Exact Match
↓
Fuzzy Match
↓
Substring Match
↓
LLM Fallback
↓
Bot Response

This hybrid architecture improves reliability while maintaining flexibility for unseen queries.

---

## 📂 Project Structure

```
project/
│── chatbot.py
│── README.md
```

---

## 🛠️ Technologies Used

- Python 3
- difflib
- random
- re (Regular Expressions)
- sys

---

## 💬 Supported Commands

Examples include:

- hello
- hi
- help
- about
- DecodeLabs
- internship
- architecture
- contact
- exit

Example:

```
You: hello

Bot: Hello! Welcome to DecodeLabs. How can I assist you with your AI journey today?
```

---

## 🔮 Future Improvements

- Integrate Google Gemini API
- Add OpenAI API support
- Store conversation history
- Web interface using Flask or Streamlit
- Voice interaction
- Database-backed knowledge base

---

## ▶️ How to Run

Clone the repository:

```bash
git clone https://github.com/yourusername/your-repository.git
```

Navigate to the project folder:

```bash
cd your-repository
```

Run the chatbot:

```bash
python chatbot.py
```

---

## 📖 Learning Outcomes

This project demonstrates:

- Rule-Based AI
- Hybrid AI Systems
- Intent Detection
- Natural Language Processing Basics
- Modular Python Programming
- AI System Architecture

---

## 👨‍💻 Author

**Rehmat Ali**

AI Intern | Computer Engineering Student

GitHub: https://github.com/rehmatali609

LinkedIn:https://www.linkedin.com/in/rehmat-ali-49a09932b
