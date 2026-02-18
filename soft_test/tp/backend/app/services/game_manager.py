from typing import Dict, Optional
from app.services.wordle import Wordle
from app.services.data_handler import get_words_processed


class GameManager:
    """Gerenciador de sessões de jogos Wordle"""

    def __init__(self):
        self._games: Dict[str, Wordle] = {}
        self._word_list: Optional[list] = None
        self._next_game_id: int = 1
    
    def _get_word_list(self) -> list:
        if self._word_list is None:
            try:
                self._word_list = get_words_processed()
            except Exception:
                self._word_list = [
                    "carro", "livro", "papel", "mundo", "tempo", "lugar","forma", "parte", "olhos"
                ]
        return self._word_list
    
    def create_game(self) -> str:
        game_id = str(self._next_game_id)
        self._next_game_id += 1
        word_list = self._get_word_list()
        self._games[game_id] = Wordle(word_list, game_id)
        return game_id
    
    def get_game(self, game_id: str) -> Optional[Wordle]:
        return self._games.get(game_id)

    def make_guess(self, game_id: str, word: str) -> dict:
        game = self.get_game(game_id)
        if not game:
            raise ValueError(f"Jogo com ID {game_id} não encontrado")
        return game.guess(word)

    def get_game_state(self, game_id: str) -> Optional[dict]:
        game = self.get_game(game_id)
        if not game:
            return None
        return {
            "game_id": game.game_id,
            "attempts": game.attempts,
            "attempts_used": len(game.attempts),
            "game_over": game.game_over,
            "won": game.won,
            "target_word": game.target_word if game.game_over else None
        }

game_manager = GameManager()
