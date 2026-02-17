
import os
import requests
import unicodedata
from app.core.config import settings


def get_words_processed() -> list[str]:
    list_words = get_words()
    return preprocess_words(list_words)


def get_words() -> list[str]:
    """
    Get words file and return the words as a list of strings
    """
    response = requests.get(settings.url_words, timeout=20)
    response.raise_for_status()

    return response.text.split('\n')


def preprocess_words(words: list[str]) -> bool:
    """
    Preprocess data
    Get all words from the words file and filter:
    - Strip
    - Filter words == 5 letters
    - Lower
    - Remove accents
    - Remove duplicates

    Then save the processed words back to the file
    Returns True for success and False for failure
    """
    words_set: set = set()

    for word in words:
        word = word.strip()
        word = remove_special_characters(word)
        if len(word) == 5:
            word = word.lower()
            word = remove_accents(word)
            words_set.add(word)

    words_list = list(words_set)
    words_list.sort()
    return words_list


def remove_accents(text: str) -> str:
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')


def remove_special_characters(text: str) -> str:
    return ''.join(char for char in text if char.isalpha())
