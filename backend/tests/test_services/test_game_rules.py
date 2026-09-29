import pytest

from app.models.game import Game
from app.services.game_rules import IllegalMove, apply_move


def make_game(
    *,
    statuses: list[str | None] | None = None,
    next_board: int | None = None,
    current_player: str = "X",
    winner: str | None = None,
) -> Game:
    return Game(
        id="test-game",
        boards=[[None for _ in range(9)] for _ in range(9)],
        statuses=statuses or [None for _ in range(9)],
        current_player=current_player,
        next_board=next_board,
        winner=winner,
    )


def test_playing_final_cell_can_win_micro_and_macro_boards() -> None:
    statuses: list[str | None] = ["X", "X", None, None, None, None, None, None, None]
    game = make_game(statuses=statuses, next_board=2)
    game.boards[2][:2] = ["X", "X"]

    apply_move(game, board_index=2, cell_index=2)

    assert game.statuses[2] == "X"
    assert game.winner == "X"
    assert game.boards[2][2] == "X"


def test_filled_macro_board_without_a_line_is_a_draw() -> None:
    statuses: list[str | None] = [None, "X", "O", "O", "X", "X", "X", "O", "O"]
    game = make_game(statuses=statuses, next_board=0, current_player="O")
    game.boards[0] = ["X", "O", "X", "O", "X", "O", "O", "X", None]

    apply_move(game, board_index=0, cell_index=8)

    assert game.statuses[0] == "draw"
    assert game.winner == "draw"


@pytest.mark.parametrize(
    ("game", "board_index", "cell_index", "message"),
    [
        (make_game(winner="X"), 0, 0, "The game is over."),
        (make_game(statuses=["X", None, None, None, None, None, None, None, None]), 0, 0,
         "That board is not available."),
    ],
)
def test_unavailable_game_and_board_moves_are_rejected(
    game: Game,
    board_index: int,
    cell_index: int,
    message: str,
) -> None:
    with pytest.raises(IllegalMove, match=message):
        apply_move(game, board_index, cell_index)


def test_occupied_cell_is_rejected() -> None:
    game = make_game()
    game.boards[0][0] = "O"

    with pytest.raises(IllegalMove, match="That cell is already marked."):
        apply_move(game, board_index=0, cell_index=0)


def test_closed_routed_board_allows_choice_of_another_open_board() -> None:
    statuses: list[str | None] = [None, "X", None, None, None, None, None, None, None]
    game = make_game(statuses=statuses, next_board=1)

    apply_move(game, board_index=0, cell_index=4)

    assert game.boards[0][4] == "X"
    assert game.next_board == 4