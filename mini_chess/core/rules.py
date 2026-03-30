from core.move import Move
from core.pieces import is_same_side, is_enemy, get_piece_type
from core.board import apply_move, find_king


BOARD_SIZE = 8


def is_inside(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


# =========================
# PSEUDO MOVE GENERATORS
# =========================

def generate_pawn_moves(board, row, col, current_player):
    moves = []

    if current_player == "white":
        forward_row = row - 1

        if is_inside(forward_row, col) and board[forward_row][col] == ".":
            moves.append(Move(row, col, forward_row, col))

        for dc in (-1, 1):
            nr, nc = row - 1, col + dc
            if is_inside(nr, nc) and is_enemy(board[nr][nc], current_player):
                moves.append(Move(row, col, nr, nc))

    else:
        forward_row = row + 1

        if is_inside(forward_row, col) and board[forward_row][col] == ".":
            moves.append(Move(row, col, forward_row, col))

        for dc in (-1, 1):
            nr, nc = row + 1, col + dc
            if is_inside(nr, nc) and is_enemy(board[nr][nc], current_player):
                moves.append(Move(row, col, nr, nc))

    return moves


def generate_rook_moves(board, row, col, current_player):
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        nr, nc = row + dr, col + dc

        while is_inside(nr, nc):
            target = board[nr][nc]

            if target == ".":
                moves.append(Move(row, col, nr, nc))
            else:
                if is_enemy(target, current_player):
                    moves.append(Move(row, col, nr, nc))
                break

            nr += dr
            nc += dc

    return moves


def generate_king_moves(board, row, col, current_player):
    moves = []
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    for dr, dc in directions:
        nr, nc = row + dr, col + dc

        if not is_inside(nr, nc):
            continue

        target = board[nr][nc]
        if target == "." or is_enemy(target, current_player):
            moves.append(Move(row, col, nr, nc))

    return moves


def get_piece_moves(board, row, col, current_player):
    piece = board[row][col]
    piece_type = get_piece_type(piece)

    if piece_type == "p":
        return generate_pawn_moves(board, row, col, current_player)
    if piece_type == "r":
        return generate_rook_moves(board, row, col, current_player)
    if piece_type == "k":
        return generate_king_moves(board, row, col, current_player)

    return []


def get_pseudo_legal_moves(state):
    if state.game_over:
        return []

    board = state.board
    current_player = state.current_player
    moves = []

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            piece = board[r][c]

            if not is_same_side(piece, current_player):
                continue

            moves.extend(get_piece_moves(board, r, c, current_player))

    return moves


# =========================
# ATTACK / CHECK
# =========================

def is_square_attacked(board, row, col, attacker_player):
    # Pawn attacks
    if attacker_player == "white":
        # white pawn attacks upward => from (row+1, col±1)
        for dc in (-1, 1):
            pr, pc = row + 1, col + dc
            if is_inside(pr, pc) and board[pr][pc] == "P":
                return True
    else:
        # black pawn attacks downward => from (row-1, col±1)
        for dc in (-1, 1):
            pr, pc = row - 1, col + dc
            if is_inside(pr, pc) and board[pr][pc] == "p":
                return True

    # Rook attacks
    rook_symbol = "R" if attacker_player == "white" else "r"
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        while is_inside(nr, nc):
            piece = board[nr][nc]
            if piece == ".":
                nr += dr
                nc += dc
                continue

            if piece == rook_symbol:
                return True
            break

    # King attacks
    king_symbol = "K" if attacker_player == "white" else "k"
    king_dirs = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    for dr, dc in king_dirs:
        nr, nc = row + dr, col + dc
        if is_inside(nr, nc) and board[nr][nc] == king_symbol:
            return True

    return False


def is_in_check(state, player):
    king_pos = find_king(state.board, player)
    if king_pos is None:
        return True

    kr, kc = king_pos
    attacker = "black" if player == "white" else "white"
    return is_square_attacked(state.board, kr, kc, attacker)


# =========================
# LEGAL MOVES
# =========================

def is_legal_move(state, move):
    player = state.current_player
    next_state = apply_move(state, move)
    return not is_in_check(next_state, player)


def get_legal_moves(state):
    pseudo_moves = get_pseudo_legal_moves(state)
    legal_moves = []

    for move in pseudo_moves:
        if is_legal_move(state, move):
            legal_moves.append(move)

    return legal_moves