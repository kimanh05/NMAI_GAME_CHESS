from core.rules import get_legal_moves


class MCTSAI:
    def choose_move(self, state):
        moves = get_legal_moves(state)
        if not moves:
            return None
        return moves[-1]