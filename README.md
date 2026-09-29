# Ultimate Tic-Tac-Toe

A browser-playable Ultimate Tic-Tac-Toe board built with the course stack: FastAPI and React/TypeScript/Vite.

## Run locally

Backend:

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
corepack pnpm install
corepack pnpm dev
```

Open the Vite URL shown in the terminal. The backend persists game state in SQLite and exposes endpoints to create a game, retrieve its current state, and submit a move. Interactive frontend play remains client-side until it is connected to these endpoints.

The API is available at `/api/v1/games`; interactive documentation is available at `/docs` when the backend is running. Set `DATABASE_URL` to change the SQLite database location.

## Rules

X starts. Each move sends the next player to the small board matching the square just played. If that destination is already won or full, the next player may choose any open board. Three marks in a row claim a small board, and three claimed boards in a row win the match.

## Checks

```bash
cd frontend && pnpm test:cov && pnpm build
cd ../backend && uv run pytest --cov=app --cov-report=term-missing:skip-covered --cov-fail-under=80
```
