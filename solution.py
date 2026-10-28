# solution.py

import string

def clean_and_group_words(text: str) -> dict[str, int]:
    """
    Takes a multi-line string, cleans punctuation, converts to lowercase,
    and returns a dictionary mapping each word to its frequency.
    """
    if not text:
        return {}

    words = text.lower().split()  
    counts: dict[str, int] = {}
    for word in words:
        # Remove punctuation and count
        clean_word = word.translate(str.maketrans('', '', string.punctuation)) 
        counts[clean_word] = counts.get(clean_word, 0) + 1
    return counts