from fastapi import APIRouter, HTTPException

from app.api.v1.models.wordle import GuessRequest, GameResponse, GuessResponse
from app.services.game_manager import game_manager

wordle_router = APIRouter()


@wordle_router.post("/games")
async def create_game():
    game_id = game_manager.create_game()
    return {"game_id": game_id}


@wordle_router.post("/games/{game_id}/guess", response_model=GuessResponse)
async def make_guess(game_id: str, guess_request: GuessRequest):
    try:
        result = game_manager.make_guess(game_id, guess_request.word.lower())
        return GuessResponse(
            game_id=result["game_id"],
            guess=result["guess"],
            result=result["attempts"][-1]["result"],
            attempts_used=result["attempts_used"],
            game_over=result["game_over"],
            won=result["won"],
            target_word=result["target_word"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@wordle_router.get("/games/{game_id}")
async def get_game_state(game_id: str):
    game_state = game_manager.get_game_state(game_id)
    if not game_state:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return GameResponse(**game_state)


