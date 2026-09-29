from fastapi.testclient import TestClient


def test_create_and_retrieve_game(client: TestClient) -> None:
    created = client.post("/api/v1/games")

    assert created.status_code == 201
    state = created.json()
    assert state["current_player"] == "X"
    assert state["next_board"] is None
    assert state["winner"] is None
    assert state["boards"] == [[None] * 9 for _ in range(9)]
    assert state["statuses"] == [None] * 9

    retrieved = client.get(f"/api/v1/games/{state['id']}")
    assert retrieved.status_code == 200
    assert retrieved.json() == state


def test_move_routes_next_turn_and_rejects_wrong_board(client: TestClient) -> None:
    game_id = client.post("/api/v1/games").json()["id"]

    moved = client.post(
        f"/api/v1/games/{game_id}/moves",
        json={"board_index": 0, "cell_index": 4},
    )
    assert moved.status_code == 200
    assert moved.json()["boards"][0][4] == "X"
    assert moved.json()["current_player"] == "O"
    assert moved.json()["next_board"] == 4

    rejected = client.post(
        f"/api/v1/games/{game_id}/moves",
        json={"board_index": 0, "cell_index": 3},
    )
    assert rejected.status_code == 409
    assert rejected.json()["detail"] == "You must play in the routed board."

    next_move = client.post(
        f"/api/v1/games/{game_id}/moves",
        json={"board_index": 4, "cell_index": 2},
    )
    assert next_move.status_code == 200
    assert next_move.json()["boards"][4][2] == "O"
    assert next_move.json()["next_board"] == 2


def test_move_reports_missing_game_and_invalid_indices(client: TestClient) -> None:
    missing = client.post(
        "/api/v1/games/unknown/moves",
        json={"board_index": 0, "cell_index": 0},
    )
    assert missing.status_code == 404

    invalid = client.post(
        "/api/v1/games/unknown/moves",
        json={"board_index": 9, "cell_index": 0},
    )
    assert invalid.status_code == 422