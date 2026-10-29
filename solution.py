# solution.py

import re
from collections import Counter

def clean_and_group_words(text: str) -> dict[str, int]:
    """
    Takes a multi-line string, keeps letters, numbers, and whitespace,
    and returns a dictionary mapping each word to its frequency.
    """
    cleaned_text = re.sub(r"[^\w\s]|_", "", text)
    words = cleaned_text.lower().split()
    return {word: count for word, count in Counter(words).items()}