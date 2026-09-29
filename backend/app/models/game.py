from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    boards: Mapped[list[list[str | None]]] = mapped_column(JSON, nullable=False)
    statuses: Mapped[list[str | None]] = mapped_column(JSON, nullable=False)
    current_player: Mapped[str] = mapped_column(String(1), nullable=False)
    next_board: Mapped[int | None] = mapped_column(Integer, nullable=True)
    winner: Mapped[str | None] = mapped_column(String(4), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def state(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "boards": self.boards,
            "statuses": self.statuses,
            "current_player": self.current_player,
            "next_board": self.next_board,
            "winner": self.winner,
        }