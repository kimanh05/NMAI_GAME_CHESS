from copy import deepcopy
from core.game_state import GameState


def clone_board(board):
    return deepcopy(board)


def clone_state(state):
    new_state = GameState(
        board=clone_board(state.board),
        current_player=state.current_player,
        winner=state.winner,
        game_over=state.game_over,
        result=state.result,
    )
    new_state.history = state.history.copy()
    return new_state


def print_board(board):
    print("   0 1 2 3 4 5 6 7")
    print("  -----------------")
    for r in range(8):
        print(f"{r}| " + " ".join(board[r]))
    print()


def get_piece_at(board, row, col):
    return board[row][col]


def set_piece_at(board, row, col, piece):
    board[row][col] = piece


def switch_player(player):
    return "black" if player == "white" else "white"


def apply_move(state, move):
    new_board = clone_board(state.board)

    moving_piece = new_board[move.sr][move.sc]
    new_board[move.er][move.ec] = moving_piece
    new_board[move.sr][move.sc] = "."

    # pawn promotion
    if moving_piece == "P" and move.er == 0:
        new_board[move.er][move.ec] = "R"
    elif moving_piece == "p" and move.er == 7:
        new_board[move.er][move.ec] = "r"

    new_state = GameState(
        board=new_board,
        current_player=switch_player(state.current_player),
        winner=None,
        game_over=False,
        result=None,
    )

    new_state.history = state.history.copy()

    return new_state


def find_king(board, player):
    target = "K" if player == "white" else "k"
    for r in range(8):
        for c in range(8):
            if board[r][c] == target:
                return (r, c)
    return None


def only_kings_left(board):
    pieces = []
    for row in board:
        for piece in row:
            if piece != ".":
                pieces.append(piece)
    return sorted(pieces) == ["K", "k"]