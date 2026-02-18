from app.services.data_handler import get_words, get_words_processed, preprocess_words, remove_accents, remove_special_characters
from app.core.config import settings
from unittest.mock import ANY
from requests.exceptions import HTTPError
import pytest

sample_data_raw = """worda
 wordb
wordc 
wórdd
wor-e
wordff
(wordg)"""
sample_data = ['worda', ' wordb', 'wordc ',
               'wórdd', 'wor-e', 'wordff', '(wordg)',]
valid_words = ['worda', 'wordb', 'wordc', 'wordd', 'wordg']


def test_get_words_processed(mocker):
    mock_get = mocker.patch('app.services.data_handler.requests.get')
    mock_get.return_value.text = sample_data_raw
    mock_get.return_value.status_code = 200

    assert get_words_processed() == valid_words
    mock_get.assert_called_once_with(settings.url_words, timeout=ANY)


def test_get_words(mocker):
    mock_get = mocker.patch('app.services.data_handler.requests.get')
    mock_get.return_value.text = sample_data_raw
    mock_get.return_value.status_code = 200

    assert get_words() == sample_data
    mock_get.assert_called_once_with(settings.url_words, timeout=ANY)


def test_get_words_failure(mocker):
    mock_get = mocker.patch('app.services.data_handler.requests.get')
    mock_get.return_value.status_code = 400
    mock_get.return_value.raise_for_status.side_effect = HTTPError(
        "400 Client Error")

    with pytest.raises(HTTPError):
        get_words()

    mock_get.assert_called_once_with(settings.url_words, timeout=ANY)


def test_preprocess_words():
    assert preprocess_words(sample_data) == valid_words


def test_remove_accents():
    assert remove_accents("no-accents") == 'no-accents'
    assert remove_accents("café") == "cafe"
    assert remove_accents("áèïõû") == "aeiou"


def test_remove_special_characters():
    assert remove_special_characters("no-accents") == 'noaccents'
    assert remove_special_characters("café") == 'café'
    assert remove_special_characters("()_-+=^~") == ''
    assert remove_special_characters("carvão") == 'carvão'
