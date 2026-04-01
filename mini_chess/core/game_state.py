class GameState:
    def __init__(self, board=None, current_player="white", winner=None, game_over=False, result=None):
        self.board = board if board is not None else self.create_initial_board()
        self.current_player = current_player
        self.winner = winner          # "white", "black", hoặc None
        self.game_over = game_over
        self.result = result          # "checkmate", "stalemate", "draw", hoặc None
        self.history = []

    def board_to_string(self):
        return "".join("".join(row) for row in self.board)

    def update_history(self):
        pos = self.board_to_string()
        self.history.append(pos)

        # 3 lần lặp -> hòa
        if self.history.count(pos) >= 3:
            self.game_over = True
            self.result = "draw"
            self.winner = None

    def create_initial_board(self):
        return [
            [".", ".", ".", "k", ".", ".", ".", "."],
            [".", ".", ".", "r", ".", ".", ".", "."],
            [".", ".", "p", "p", "p", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", "P", "P", "P", ".", ".", "."],
            [".", ".", ".", "R", ".", ".", ".", "."],
            [".", ".", ".", "K", ".", ".", ".", "."],
        ]