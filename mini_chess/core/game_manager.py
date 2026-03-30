from core.board import apply_move, only_kings_left
from core.rules import get_legal_moves, is_in_check
from config import (
    MODE_HUMAN_VS_HUMAN,
    MODE_HUMAN_VS_ALPHABETA,
    MODE_HUMAN_VS_MCTS,
    MODE_AI_VS_AI,
)


class GameManager:
    def __init__(self, initial_state, mode=MODE_HUMAN_VS_HUMAN, white_ai=None, black_ai=None):
        self.initial_state = initial_state
        self.state = initial_state
        self.mode = mode
        self.white_ai = white_ai
        self.black_ai = black_ai
        self.update_game_status()

    def reset(self, new_state=None):
        if new_state is None:
            from core.game_state import GameState
            self.state = GameState()
            self.initial_state = self.state
        else:
            self.state = new_state
            self.initial_state = new_state

        self.update_game_status()

    def set_mode(self, mode, white_ai=None, black_ai=None):
        self.mode = mode
        self.white_ai = white_ai
        self.black_ai = black_ai

    def get_state(self):
        return self.state

    def get_valid_moves(self):
        return get_legal_moves(self.state)

    def is_valid_move(self, move):
        return move in self.get_valid_moves()

    def make_move(self, move):
        if self.state.game_over:
            return False

        if move is None:
            return False

        if not self.is_valid_move(move):
            return False

        self.state = apply_move(self.state, move)
        self.update_game_status()
        return True

    def update_game_status(self):
        if only_kings_left(self.state.board):
            self.state.game_over = True
            self.state.winner = None
            self.state.result = "draw"
            return

        legal_moves = get_legal_moves(self.state)

        if len(legal_moves) == 0:
            current_player = self.state.current_player

            if is_in_check(self.state, current_player):
                self.state.game_over = True
                self.state.winner = "black" if current_player == "white" else "white"
                self.state.result = "checkmate"
            else:
                self.state.game_over = True
                self.state.winner = None
                self.state.result = "stalemate"
            return

        self.state.game_over = False
        self.state.winner = None
        self.state.result = None

    def is_game_over(self):
        return self.state.game_over

    def get_winner(self):
        return self.state.winner

    def get_result(self):
        return self.state.result

    def is_in_check(self, player=None):
        if player is None:
            player = self.state.current_player
        return is_in_check(self.state, player)

    def is_human_turn(self):
        current_player = self.state.current_player

        if self.mode == MODE_HUMAN_VS_HUMAN:
            return True

        if self.mode == MODE_HUMAN_VS_ALPHABETA:
            return current_player == "white"

        if self.mode == MODE_HUMAN_VS_MCTS:
            return current_player == "white"

        if self.mode == MODE_AI_VS_AI:
            return False

        return True

    def get_current_ai(self):
        current_player = self.state.current_player
        return self.white_ai if current_player == "white" else self.black_ai

    def should_ai_move(self):
        return (not self.state.game_over) and (not self.is_human_turn())