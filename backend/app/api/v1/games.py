from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.game import Game
from app.schemas.game import GameResponse, MoveRequest
from app.services.game_rules import GameNotFound, IllegalMove
from app.services.games import create_game, get_game, play_game_move

router = APIRouter(prefix="/games", tags=["games"])


def _response(game: Game) -> GameResponse:
    return GameResponse(**game.state())


@router.post("", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game_endpoint(session: Annotated[Session, Depends(get_db)]) -> GameResponse:
    return _response(create_game(session))


@router.get("/{game_id}", response_model=GameResponse)
def get_game_endpoint(
    game_id: str,
    session: Annotated[Session, Depends(get_db)],
) -> GameResponse:
    try:
        return _response(get_game(session, game_id))
    except GameNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.post("/{game_id}/moves", response_model=GameResponse)
def play_move_endpoint(
    game_id: str,
    move: MoveRequest,
    session: Annotated[Session, Depends(get_db)],
) -> GameResponse:
    try:
        game = play_game_move(session, game_id, move.board_index, move.cell_index)
    except GameNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except IllegalMove as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return _response(game)