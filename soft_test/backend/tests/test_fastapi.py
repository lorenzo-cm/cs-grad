import pytest

from app.services.game_manager import game_manager
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def game_id(client: TestClient):
    response = client.post("/api/v1/wordle/games")

    data = response.json()
    return data["game_id"]


class TestAPIHealthCheck:
    def test_read_root(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestAPICreateGame:
    def teardown_method(self, method):
        # Reset after each test to isolate the mocker to this test class
        game_manager._word_list = None

    def test_create_game(self, client: TestClient):
        response = client.post("/api/v1/wordle/games")
        assert response.status_code == 200

        data = response.json()
        assert "game_id" in data
        assert isinstance(data["game_id"], str)

    def test_create_game_multiple(self, client: TestClient):
        response1 = client.post("/api/v1/wordle/games")
        response2 = client.post("/api/v1/wordle/games")

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = response1.json()
        data2 = response2.json()

        assert data1["game_id"] != data2["game_id"]
        assert isinstance(data1["game_id"], str)
        assert isinstance(data2["game_id"], str)

    def test_create_game_recover_from_word_list_fail(self, client: TestClient, mocker):
        # Simulate a failure in get_words_processed
        mocker.patch(
            "app.services.game_manager.get_words_processed",
            side_effect=Exception("Mocked get words exception")
        )

        # Reset the word list to None to force a reload
        game_manager._word_list = None

        response = client.post("/api/v1/wordle/games")
        assert response.status_code == 200

        data = response.json()
        assert "game_id" in data
        assert isinstance(data["game_id"], str)


class TestAPIMakeGuess:
    def test_make_guess(self, client: TestClient, game_id):
        response = client.post(
            f"/api/v1/wordle/games/{game_id}/guess", json={"word": "arroz"}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["game_id"] == game_id
        assert data["guess"] == "arroz"
        assert isinstance(data["result"], list)
        assert isinstance(data["attempts_used"], int)
        assert isinstance(data["game_over"], bool)
        assert isinstance(data["won"], bool)

    def test_make_guess_invalid_id(self, client: TestClient):
        response = client.post(
            "/api/v1/wordle/games/12345/guess", json={"word": "arroz"}
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Jogo com ID 12345 não encontrado"}


class TestAPIGetGameState:
    def test_get_game_state(self, client: TestClient, game_id):
        response = client.get(f"/api/v1/wordle/games/{game_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["game_id"] == game_id
        assert isinstance(data["attempts"], list)
        assert isinstance(data["attempts_used"], int)
        assert isinstance(data["game_over"], bool)
        assert isinstance(data["won"], bool)
        assert "target_word" in data

    def test_get_game_state_invalid_id(self, client: TestClient):
        response = client.get("/api/v1/wordle/games/12345")
        assert response.status_code == 404
        assert response.json() == {"detail": "Jogo não encontrado"}
