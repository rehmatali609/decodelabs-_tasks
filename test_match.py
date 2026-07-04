from chatbot import sanitize_input, match_intent, INTENT_RESPONSE_MAP
s = sanitize_input('tell me about decodelabs internship')
print('sanitized:', repr(s))
print('keys:', list(INTENT_RESPONSE_MAP.keys()))
print('match:', match_intent(s))
