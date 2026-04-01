from core.rules import get_legal_moves
from core.board import apply_move


class AlphaBetaAI:
    def __init__(self, depth=3):
        self.depth = depth

    def choose_move(self, state):
        moves = get_legal_moves(state)
        if not moves:
            return None

        # sắp xếp nước đi: ưu tiên nước ăn quân trước để alpha-beta cắt tỉa tốt hơn
        moves = self.order_moves(state, moves)

        # white muốn maximize, black muốn minimize
        maximizing = (state.current_player == "white")

        best_move = None

        if maximizing:
            best_score = float("-inf")
            alpha = float("-inf")
            beta = float("inf")

            for move in moves:
                next_state = apply_move(state, move)
                score = self.alphabeta(
                    next_state,
                    depth=self.depth - 1,
                    alpha=alpha,
                    beta=beta,
                    maximizing=False
                )

                if score > best_score:
                    best_score = score
                    best_move = move

                alpha = max(alpha, best_score)

        else:
            best_score = float("inf")
            alpha = float("-inf")
            beta = float("inf")

            for move in moves:
                next_state = apply_move(state, move)
                score = self.alphabeta(
                    next_state,
                    depth=self.depth - 1,
                    alpha=alpha,
                    beta=beta,
                    maximizing=True
                )

                if score < best_score:
                    best_score = score
                    best_move = move

                beta = min(beta, best_score)

        return best_move

    def alphabeta(self, state, depth, alpha, beta, maximizing):
        # terminal hoặc hết depth
        if depth == 0 or state.game_over:
            return self.evaluate(state)

        moves = get_legal_moves(state)

        if not moves:
            return self.evaluate(state)

        moves = self.order_moves(state, moves)

        if maximizing:
            value = float("-inf")
            for move in moves:
                next_state = apply_move(state, move)
                value = max(
                    value,
                    self.alphabeta(next_state, depth - 1, alpha, beta, False)
                )
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value

        else:
            value = float("inf")
            for move in moves:
                next_state = apply_move(state, move)
                value = min(
                    value,
                    self.alphabeta(next_state, depth - 1, alpha, beta, True)
                )
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def evaluate(self, state):
        """
        Score > 0  => tốt cho white
        Score < 0  => tốt cho black
        """

        # trạng thái kết thúc
        if state.game_over:
            if state.result == "draw" or state.result == "stalemate":
                return 0

            if state.result == "checkmate":
                if state.winner == "white":
                    return 100000
                elif state.winner == "black":
                    return -100000
                return 0

        # material score
        piece_value = {
            "P": 100,
            "R": 500,
            "K": 10000,
            "p": -100,
            "r": -500,
            "k": -10000,
        }

        score = 0
        for row in state.board:
            for piece in row:
                if piece != ".":
                    score += piece_value.get(piece, 0)

        # mobility bonus nhỏ
        current_moves = len(get_legal_moves(state))
        if state.current_player == "white":
            score += current_moves * 2
        else:
            score -= current_moves * 2

        # pawn advancement bonus
        score += self.pawn_advancement_score(state)

        return score

    def pawn_advancement_score(self, state):
        """
        Thưởng cho pawn đi gần tới cuối bàn hơn.
        White đi lên => row nhỏ hơn là tốt.
        Black đi xuống => row lớn hơn là tốt.
        """
        bonus = 0

        for r in range(8):
            for c in range(8):
                piece = state.board[r][c]
                if piece == "P":
                    # càng gần hàng 0 càng tốt
                    bonus += (7 - r) * 5
                elif piece == "p":
                    # càng gần hàng 7 càng tốt
                    bonus -= r * 5

        return bonus

    def order_moves(self, state, moves):
        """
        Ưu tiên:
        1. nước ăn quân
        2. nước đi thường
        """
        scored_moves = []

        for move in moves:
            target_piece = state.board[move.er][move.ec]

            # quân đích càng giá trị thì càng ưu tiên
            capture_score = self.capture_value(target_piece)
            scored_moves.append((capture_score, move))

        # sort giảm dần để nước ăn quân mạnh đi trước
        scored_moves.sort(key=lambda x: x[0], reverse=True)

        return [move for _, move in scored_moves]

    def capture_value(self, piece):
        values = {
            "P": 100,
            "R": 500,
            "K": 10000,
            "p": 100,
            "r": 500,
            "k": 10000,
            ".": 0,
        }
        return values.get(piece, 0)