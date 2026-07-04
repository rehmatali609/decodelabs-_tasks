"""
DecodeLabs AI Chatbot - Hybrid Architecture (Rule-Based + LLM Fallback)
Author: Senior AI Architect / AI Intern
Description: A production-ready logic engine designed for the DecodeLabs internship.
             Implements cascaded deterministic matching with a generative LLM safety net.
"""

import sys
import random
import difflib
import re

# ==============================================================================
# KNOWLEDGE BASE (Dynamic Response Dictionary)
# ==============================================================================
INTENT_RESPONSE_MAP = {
    "hello": [
        "Hello! Welcome to DecodeLabs. How can I assist you with your AI journey today?",
        "Greetings! DecodeLabs deterministic agent online. What do you need?",
        "Hi there! Ready to engineer some logic today?"
    ],
    "hi": [
        "Hi! Welcome to the DecodeLabs agent. What's on your mind?",
        "Hello! How can I help you navigate your internship projects?"
    ],
    "help": [
        "I support queries like: 'hello', 'about', 'internship', 'architecture', 'contact', and 'exit'.",
        "Need a hand? Try asking me about 'DecodeLabs', our 'internship', or type 'exit' to leave."
    ],
    "about": [
        "DecodeLabs is a premier educational and research incubator focusing on agentic AI, software engineering, and internships.",
        "DecodeLabs runs hands-on internship tracks that teach production-ready AI pipelines and engineering best practices."
    ],
    "decodelabs": [
        "DecodeLabs is a premier educational and research incubator focusing on agentic AI, software engineering, and internships.",
        "You can learn about DecodeLabs' internship opportunities, projects, and open-source resources on our site or GitHub."
    ],
    "decode labs": [
        "DecodeLabs (\"Decode Labs\") offers internship programs and hands-on projects in AI and software engineering.",
        "Look for our internship track descriptions or contact careers@decodelabs.ai for more details."
    ],
    "architecture": [
        "Just like designing circuits or routing systems, building AI guardrails requires precise, deterministic control flow.",
        "This system uses cascaded logic: Exact Match -> Fuzzy Match -> Substring Search -> Probabilistic LLM Fallback."
    ],
    "internship": [
        "The DecodeLabs internship program provides hands-on experience in building production-ready AI pipelines.",
        "You'll be moving from foundational logic engines to complex probabilistic models during this track."
    ],
    "contact": [
        "You can reach out to us by emailing careers@decodelabs.ai.",
        "Drop us a line at decodelabs.tech@gmail.com or check our GitHub workspace!"
    ],
    "exit": [
        "Shutting down core logic loop... Goodbye!",
        "Session terminated. See you next time!",
        "Exiting process. Have a great day!"
    ]
}

# Static fallbacks if the Generative API is completely unreachable
STATIC_FALLBACKS = [
    "I do not understand that command, and my neural link is offline. Type 'help'.",
    "My deterministic guardrails don't recognize that input. Try asking for 'help'."
]

# ==============================================================================
# GENERATIVE AI FALLBACK LAYER (The Probabilistic Core)
# ==============================================================================
def call_llm_api(user_input: str) -> str:
    """
    Acts as the probabilistic safety net when all deterministic guardrails fail.
    
    NOTE: To make this live, install a library (e.g., pip install google-generativeai)
    and replace this mock function with actual API connection code.
    """
    try:
        # --- FUTURE API INTEGRATION GOES HERE ---
        # Example for Gemini API:
        # import google.generativeai as genai
        # genai.configure(api_key="YOUR_API_KEY")
        # model = genai.GenerativeModel('gemini-1.5-flash')
        # response = model.generate_content(f"You are a DecodeLabs assistant. Reply briefly to: {user_input}")
        # return response.text
        
        # Mock LLM response for testing the architecture without an API key
        return f"[Simulated LLM API Response]: I don't have a hardcoded rule for '{user_input}', but as an AI, I can help you find out more. What specifically would you like to know?"
        
    except Exception as e:
        # Ultimate fail-safe if the API request times out or fails
        return random.choice(STATIC_FALLBACKS)

# ==============================================================================
# PROCESS STAGE (Cascaded Matching Strategy)
# ==============================================================================
def match_intent(sanitized_input: str) -> str:
    """
    Matches intent using a tiered priority system:
    1) Exact O(1) lookup
    2) Fuzzy closest-key match
    3) Substring containment
    4) Generative LLM fallback
    """
    if not sanitized_input:
        return random.choice(STATIC_FALLBACKS)

    # Tier 1: Exact O(1) lookup
    if sanitized_input in INTENT_RESPONSE_MAP:
        return random.choice(INTENT_RESPONSE_MAP[sanitized_input])

    # Tier 2: Fuzzy match using difflib (Catches typos like "hlp" instead of "help")
    close = difflib.get_close_matches(sanitized_input, INTENT_RESPONSE_MAP.keys(), n=1, cutoff=0.75)
    if close:
        return random.choice(INTENT_RESPONSE_MAP[close[0]])

    # Tier 3: Substring fallback (Catches sentences like "Tell me about the internship")
    # Collect all keys that match as whole words, then select the most
    # specific (longest) key to improve accuracy when multiple keys match.
    matches = []
    for key in INTENT_RESPONSE_MAP.keys():
        pattern = r"\b" + re.escape(key) + r"\b"
        if re.search(pattern, sanitized_input):
            matches.append(key)

    if matches:
        # Prefer longer keys (more specific). If tied, prefer the key that
        # appears later in the user's input (assumes specificity towards the end).
        best = max(matches, key=lambda k: (len(k), sanitized_input.find(k)))
        return random.choice(INTENT_RESPONSE_MAP[best])

    # Tier 4: No deterministic match found — route to the Generative LLM
    return call_llm_api(sanitized_input)

# ==============================================================================
# INPUT & OUTPUT STAGES
# ==============================================================================
def sanitize_input(raw_input: str) -> str:
    if raw_input is None:
        return ""
    return raw_input.lower().strip()

def generate_output(response: str) -> None:
    print(f"\nBot: {response}\n")

# ==============================================================================
# RUN LOOP (The Heartbeat)
# ==============================================================================
def run_chatbot() -> None:
    print("=" * 70)
    print("DecodeLabs Hybrid AI Agent initialized.")
    print("Architecture: Deterministic Dictionary -> LLM Fallback API")
    print("Type your message below. Type 'exit' to terminate.")
    print("=" * 70 + "\n")
    
    while True:
        try:
            # 1. INPUT
            raw_user_input = input("You: ")
            sanitized_input = sanitize_input(raw_user_input)
            
            # 2. PROCESS
            response = match_intent(sanitized_input)
            
            # 3. OUTPUT
            generate_output(response)
            
            # 4. CLEAN EXIT
            if "exit" in sanitized_input:
                break
                
        except (KeyboardInterrupt, EOFError):
            print("\n\nBot: Manual interrupt detected. Shutting down systems. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    run_chatbot()