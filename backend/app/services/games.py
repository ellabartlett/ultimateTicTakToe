from sqlalchemy.orm import Session

from app.models.game import Game
from app.repositories import games as game_repository
from app.services.game_rules import GameNotFound, apply_move, new_game_state


def create_game(session: Session) -> Game:
    return game_repository.create_game(session, new_game_state())


def get_game(session: Session, game_id: str) -> Game:
    game = game_repository.get_game(session, game_id)
    if game is None:
        raise GameNotFound("Game not found.")
    return game


def play_game_move(session: Session, game_id: str, board_index: int, cell_index: int) -> Game:
    game = get_game(session, game_id)
    apply_move(game, board_index, cell_index)
    return game_repository.save_game(session, game)