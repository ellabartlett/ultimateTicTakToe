from app.models.game import Game

LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


class IllegalMove(ValueError):
    pass


class GameNotFound(LookupError):
    pass


def new_game_state() -> dict[str, object]:
    return {
        "boards": [[None for _ in range(9)] for _ in range(9)],
        "statuses": [None for _ in range(9)],
        "current_player": "X",
        "next_board": None,
        "winner": None,
    }


def _line_winner(cells: list[str | None]) -> str | None:
    for first, second, third in LINES:
        mark = cells[first]
        if mark is not None and mark == cells[second] == cells[third]:
            return mark
    return None


def _board_is_open(game: Game, board_index: int) -> bool:
    return game.statuses[board_index] is None and not all(game.boards[board_index])


def apply_move(game: Game, board_index: int, cell_index: int) -> None:
    if game.winner is not None:
        raise IllegalMove("The game is over.")
    if not _board_is_open(game, board_index):
        raise IllegalMove("That board is not available.")
    if (
        game.next_board is not None
        and _board_is_open(game, game.next_board)
        and game.next_board != board_index
    ):
        raise IllegalMove("You must play in the routed board.")
    if game.boards[board_index][cell_index] is not None:
        raise IllegalMove("That cell is already marked.")

    boards = [board.copy() for board in game.boards]
    statuses = list(game.statuses)
    boards[board_index][cell_index] = game.current_player
    board_winner = _line_winner(boards[board_index])
    if board_winner is not None:
        statuses[board_index] = board_winner
    elif all(boards[board_index]):
        statuses[board_index] = "draw"

    game.boards = boards
    game.statuses = statuses
    macro_cells = [status if status != "draw" else None for status in statuses]
    macro_winner = _line_winner(macro_cells)
    if macro_winner is not None:
        game.winner = macro_winner
    elif all(status is not None for status in statuses):
        game.winner = "draw"

    game.current_player = "O" if game.current_player == "X" else "X"
    game.next_board = cell_index if _board_is_open(game, cell_index) else None