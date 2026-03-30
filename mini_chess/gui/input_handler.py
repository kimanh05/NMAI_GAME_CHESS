from core.move import Move

BOARD_SIZE = 8
CELL_SIZE = 60


class InputHandler:
    def __init__(self):
        self.selected_pos = None
        self.highlight_moves = []

    def clear_selection(self):
        self.selected_pos = None
        self.highlight_moves = []

    def get_board_position(self, mouse_pos):
        x, y = mouse_pos

        if x < 0 or y < 0 or x >= BOARD_SIZE * CELL_SIZE or y >= BOARD_SIZE * CELL_SIZE:
            return None

        col = x // CELL_SIZE
        row = y // CELL_SIZE

        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return (row, col)
        return None

    def handle_click(self, mouse_pos, manager):
        pos = self.get_board_position(mouse_pos)
        if pos is None:
            return None

        row, col = pos
        state = manager.get_state()
        piece = state.board[row][col]

        if self.selected_pos is None:
            if piece == ".":
                return None

            if state.current_player == "white" and not piece.isupper():
                return None
            if state.current_player == "black" and not piece.islower():
                return None

            self.selected_pos = pos
            all_legal_moves = manager.get_valid_moves()
            self.highlight_moves = [
                move for move in all_legal_moves
                if move.sr == row and move.sc == col
            ]
            return None

        if self.selected_pos == pos:
            self.clear_selection()
            return None

        sr, sc = self.selected_pos
        move = Move(sr, sc, row, col)

        self.clear_selection()
        return move