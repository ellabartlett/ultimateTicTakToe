from sqlalchemy.orm import Session

from app.models.game import Game


def create_game(session: Session, state: dict[str, object]) -> Game:
    game = Game(**state)
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


def get_game(session: Session, game_id: str) -> Game | None:
    return session.get(Game, game_id)


def save_game(session: Session, game: Game) -> Game:
    session.add(game)
    session.commit()
    session.refresh(game)
    return game