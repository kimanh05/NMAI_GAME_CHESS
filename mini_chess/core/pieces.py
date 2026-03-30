WHITE_PIECES = {"P", "R", "K"}
BLACK_PIECES = {"p", "r", "k"}
EMPTY = "."


def is_empty(piece):
    return piece == EMPTY


def is_white_piece(piece):
    return piece in WHITE_PIECES


def is_black_piece(piece):
    return piece in BLACK_PIECES


def is_same_side(piece, player):
    if player == "white":
        return is_white_piece(piece)
    return is_black_piece(piece)


def is_enemy(piece, player):
    if is_empty(piece):
        return False
    if player == "white":
        return is_black_piece(piece)
    return is_white_piece(piece)


def get_piece_type(piece):
    return piece.lower()


def get_piece_owner(piece):
    if is_white_piece(piece):
        return "white"
    if is_black_piece(piece):
        return "black"
    return None