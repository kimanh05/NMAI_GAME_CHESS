class GameState:
    def __init__(self, board=None, current_player="white", winner=None, game_over=False, result=None):
        self.board = board if board is not None else self.create_initial_board()
        self.current_player = current_player
        self.winner = winner
        self.game_over = game_over
        self.result = result
        self.history = []

        # lưu trạng thái ban đầu
        self.update_history()

    def board_to_string(self):
        board_str = "".join("".join(row) for row in self.board)
        return board_str + "_" + self.current_player

    def update_history(self):
        pos = self.board_to_string()
        self.history.append(pos)

        if self.history.count(pos) >= 3:
            self.game_over = True
            self.result = "threefold_repetition"
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