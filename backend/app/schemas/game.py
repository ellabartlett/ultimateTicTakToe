from typing import Literal

from pydantic import BaseModel, Field

Player = Literal["X", "O"]
BoardStatus = Literal["X", "O", "draw"] | None
GameResult = Literal["X", "O", "draw"] | None


class GameResponse(BaseModel):
    id: str
    boards: list[list[Player | None]]
    statuses: list[BoardStatus]
    current_player: Player
    next_board: int | None
    winner: GameResult


class MoveRequest(BaseModel):
    board_index: int = Field(ge=0, le=8)
    cell_index: int = Field(ge=0, le=8)