import math
import random
from core.rules import get_legal_moves
from core.board import apply_move, clone_state


# =========================
# NODE
# =========================
class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move

        self.children = []
        self.visits = 0
        self.wins = 0

        self.untried_moves = get_legal_moves(state)

    def best_child(self, c=1.4):
        return max(
            self.children,
            key=lambda n: (
                (n.wins / n.visits if n.visits > 0 else 0) +
                c * math.sqrt(math.log(self.visits + 1) / (n.visits + 1e-6))
            )
        )


# =========================
# MCTS AI
# =========================
class MCTSAI:
    def __init__(self, iterations=600):
        self.iterations = iterations

    def choose_move(self, state):
        root = Node(clone_state(state))

        if not root.untried_moves:
            return None

        root_player = state.current_player

        for _ in range(self.iterations):
            node = root
            sim_state = clone_state(state)

            # =========================
            # 1. SELECTION
            # =========================
            while node.children and not node.untried_moves:
                node = node.best_child()
                sim_state = apply_move(sim_state, node.move)

            # =========================
            # 2. EXPANSION
            # =========================
            if node.untried_moves:
                move = random.choice(node.untried_moves)
                node.untried_moves.remove(move)

                sim_state = apply_move(sim_state, move)

                child = Node(clone_state(sim_state), node, move)
                node.children.append(child)
                node = child

            # =========================
            # 3. SIMULATION (SMART)
            # =========================
            winner = self.rollout(sim_state)

            # =========================
            # 4. BACKPROPAGATION
            # =========================
            while node:
                node.visits += 1
                if winner == root_player:
                    node.wins += 1
                elif winner is None:
                    node.wins += 0.5
                node = node.parent

        # chọn move tốt nhất
        best = max(root.children, key=lambda n: n.visits)
        return best.move

    # =========================
    # SMART ROLLOUT
    # =========================
    def rollout(self, state, max_depth=10):
        for _ in range(max_depth):
            moves = get_legal_moves(state)
            if not moves:
                break

            # ưu tiên ăn quân
            best_moves = []
            best_score_gain = -999
            for m in moves:
                temp_state = apply_move(clone_state(state), m)
                score_gain = self.material_score(temp_state) - self.material_score(state)
                if score_gain > best_score_gain:
                    best_score_gain = score_gain
                    best_moves = [m]
                elif score_gain == best_score_gain:
                    best_moves.append(m)

            if best_moves and best_score_gain > 0:
                move = random.choice(best_moves)
            else:
                move = random.choice(moves)

            state = apply_move(state, move)

            # nếu game over thì dừng
            if state.game_over:
                break

        # quyết định người thắng dựa trên material score
        final_score = self.material_score(state)
        if final_score > 0:
            return "white"
        elif final_score < 0:
            return "black"
        return None

    # =========================
    # HEURISTIC MATERIAL SCORE
    # =========================
    def material_score(self, state):
        piece_value = {
            'P': 1, 'R': 5, 'K': 100,
            'p': -1, 'r': -5, 'k': -100
        }

        score = 0
        for row in state.board:
            for p in row:
                if p != '.':
                    score += piece_value.get(p, 0)
        return score
