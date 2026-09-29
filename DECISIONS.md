# Decisions

## 2026-09-28: Client-side game rules for the first slice

The game rules live in `frontend/src/game.ts` and are pure functions because the first product requirement is a local, two-player browser game. This keeps routing and win behavior directly testable and leaves the minimal FastAPI service available for a later persistence feature.

## 2026-09-28: Any-board exception

When the routed small board is already claimed or full, the next player may select any open small board. This follows the standard Ultimate Tic-Tac-Toe rule and avoids an unplayable turn.

## 2026-09-29: Persistent game API

The FastAPI backend persists game state in SQLite and validates moves in a service layer, with repositories owning database operations and API schemas defining the HTTP contract. The browser still runs its existing local game state; connecting it to the API is a separate frontend change.
