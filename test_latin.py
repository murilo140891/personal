import re

def is_latin(text):
    text_lower = text.lower()
    # Use regex for word boundaries to avoid partial matches
    english_words = ["the", "of", "to", "and", "is", "that", "it", "for", "by", "with", "whether", "objection", "reply", "answer", "on", "contrary"]
    latin_words = ["et", "in", "ad", "non", "ut", "sed", "est", "quod", "de", "cum", "per", "respondeo", "dicendum", "praeterea", "videtur", "ergo"]
    
    english_score = 0
    latin_score = 0
    
    # Simple tokenization
    tokens = re.findall(r'\b[a-z]+\b', text_lower)
    token_set = set(tokens)
    
    for word in english_words:
        if word in token_set:
            english_score += 1
            print(f"Matched English: {word}")
            
    for word in latin_words:
        if word in token_set:
            latin_score += 1
            print(f"Matched Latin: {word}")
            
    print(f"Score - English: {english_score}, Latin: {latin_score}")

    # Strong preference checks
    if english_score > 0 and latin_score == 0:
        return False
    if latin_score > 0 and english_score == 0:
        return True
    
    return latin_score >= english_score

text_english = "FIRST PART (FP: Questions 1-119)"
print(f"Testing: '{text_english}' -> {is_latin(text_english)}")

text_nav = "To place our purpose within proper limits..."
print(f"Testing: '{text_nav}' -> {is_latin(text_nav)}")

