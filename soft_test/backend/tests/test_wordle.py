import pytest
from unittest.mock import patch
from app.services import Wordle


@pytest.fixture
def word_list():
    return ["apple", "grape", "peach", "berry", "melon"]


@pytest.fixture
def game_id():
    return 1


@pytest.fixture
def wordle_game(word_list, game_id):
    with patch("random.choice", return_value="apple"):
        return Wordle(word_list, game_id)


@pytest.fixture
def wordle_game_custom_target(word_list, game_id):

    def _create_game(target_word):
        with patch("random.choice", return_value=target_word):
            return Wordle(word_list, game_id)

    return _create_game


class TestWordleInitialization:
    def test_wordle_initialization(self, wordle_game, word_list, game_id):
        assert wordle_game.game_id == game_id
        assert wordle_game.word_list == word_list
        assert wordle_game.target_word == "apple"
        assert wordle_game.attempts == []
        assert wordle_game.max_attempts == 6
        assert wordle_game.game_over is False
        assert wordle_game.won is False


class TestWordleGuessValidation:
    def test_guess_invalid_length(self, wordle_game):
        with pytest.raises(ValueError):
            wordle_game.guess("abc")

        with pytest.raises(ValueError):
            wordle_game.guess("abcdef")

    def test_guess_non_alpha(self, wordle_game):
        with pytest.raises(ValueError):
            wordle_game.guess("abc12")

    def test_guess_not_in_word_list(self, wordle_game):
        with pytest.raises(ValueError):
            wordle_game.guess("hello")

    def test_guess_with_whitespace(self, wordle_game):
        result = wordle_game.guess(" grape ")
        assert result["guess"] == "grape"


class TestWordleGameLogic:
    def test_correct_guess_wins_game(self, wordle_game):
        result = wordle_game.guess("apple")

        assert result["won"] is True
        assert result["game_over"] is True
        assert result["target_word"] == "apple"
        assert len(result["attempts"]) == 1
        assert result["attempts"][0]["result"] == ["correct"] * 5

    def test_incorrect_guess_continues_game(self, wordle_game):
        result = wordle_game.guess("grape")

        assert result["won"] is False
        assert result["game_over"] is False
        assert result["target_word"] is None
        assert len(result["attempts"]) == 1

    def test_max_attempts_game_over(self, wordle_game):
        guesses = ["grape", "peach", "berry", "melon", "grape"]

        for guess in guesses:
            result = wordle_game.guess(guess)

        assert result["game_over"] is False

        result = wordle_game.guess("grape")
        assert result["game_over"] is True
        assert result["won"] is False
        assert result["target_word"] == "apple"

    def test_check_guess_all_correct(self, wordle_game_custom_target):
        game = wordle_game_custom_target("apple")
        result = game._check_guess("apple")
        assert result == ["correct", "correct", "correct", "correct", "correct"]

    def test_check_guess_mixed_results(self, wordle_game_custom_target):
        game = wordle_game_custom_target("apple")
        result = game._check_guess("grape")
        assert result == ["not present", "not present", "present", "present", "correct"]

    def test_check_guess_repeated_letters_target_and_guess(
        self, wordle_game_custom_target
    ):
        game = wordle_game_custom_target("apple")
        result = game._check_guess("hippo")
        assert result == [
            "not present",
            "not present",
            "correct",
            "present",
            "not present",
        ]

    def test_check_guess_repeated_letters_in_guess(self, wordle_game_custom_target):
        game = wordle_game_custom_target("plane")
        result = game._check_guess("apple")
        assert result == ["present", "present", "not present", "present", "correct"]

    def test_check_guess_no_matches(self, wordle_game_custom_target):
        game = wordle_game_custom_target("apple")
        result = game._check_guess("storm")
        assert result == [
            "not present",
            "not present",
            "not present",
            "not present",
            "not present",
        ]


class TestWordleGameFlow:
    def test_multiple_guesses_tracking(self, wordle_game):
        wordle_game.guess("grape")
        wordle_game.guess("peach")
        result = wordle_game.guess("berry")

        assert len(result["attempts"]) == 3
        assert result["attempts_used"] == 3
        assert result["attempts"][0]["guess"] == "grape"
        assert result["attempts"][1]["guess"] == "peach"
        assert result["attempts"][2]["guess"] == "berry"

    def test_game_state_after_win(self, wordle_game):
        wordle_game.guess("grape")
        result = wordle_game.guess("apple")

        assert result["game_over"] is True
        assert result["won"] is True

        with pytest.raises(ValueError):
            wordle_game.guess("peach")

    def test_return_info_structure(self, wordle_game):
        result = wordle_game.guess("grape")

        required_keys = [
            "game_id",
            "guess",
            "attempts",
            "attempts_used",
            "target_word",
            "game_over",
            "won",
        ]

        for key in required_keys:
            assert key in result

        assert isinstance(result["attempts"], list)
        assert isinstance(result["attempts_used"], int)
        assert isinstance(result["game_over"], bool)
        assert isinstance(result["won"], bool)
