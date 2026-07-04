from chatbot import sanitize_input, match_intent

examples = [
    'DecodeLabs',
    'tell me about DecodeLabs',
    'tell me about decodelabs internship',
    'hello',
]

for ex in examples:
    s = sanitize_input(ex)
    print('input:', ex)
    print('sanitized:', repr(s))
    print('response:', match_intent(s))
    print('-' * 40)
