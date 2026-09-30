from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.games import router as games_router
from app.core.database import Base, engine
from app.models.game import Game  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Ultimate Tic-Tac-Toe API", version="0.1.0", lifespan=lifespan)
app.include_router(games_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
