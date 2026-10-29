# test_solution.py
from solution import clean_and_group_words


def test_empty_string():
    assert clean_and_group_words("") == {}


def test_basic_counting():
    # Should normalize case and strip standard trailing punctuation
    result = clean_and_group_words("Hello,     world! Hello.")
    assert result.get("hello", 0) == 2
    assert result.get("world", 0) == 1


def test_comprehensive_normalization():
    text = "Apple, banana apple! ORANGE. banana,"
    result = clean_and_group_words(text)

    expected = {"apple": 2, "banana": 2, "orange": 1}
    assert result == expected
