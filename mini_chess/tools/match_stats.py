# tools/match_stats.py
# Tool chạy nhiều trận để thống kê AlphaBeta vs MCTS

import csv
from core.game_state import GameState
from core.game_manager import GameManager
from config import MODE_AI_VS_AI

try:
    from ai.alphabeta import AlphaBetaAI
except:
    AlphaBetaAI = None

try:
    from ai.mcts import MCTSAI
except:
    MCTSAI = None


def create_match():
    state = GameState()
    white_ai = AlphaBetaAI()
    black_ai = MCTSAI()

    return GameManager(
        state,
        mode=MODE_AI_VS_AI,
        white_ai=white_ai,
        black_ai=black_ai
    )


def play_one_game():
    manager = create_match()

    while not manager.is_game_over():
        ai = manager.get_current_ai()
        move = ai.choose_move(manager.get_state())
        manager.make_move(move)

    state = manager.get_state()

    # tùy project bạn chỉnh winner ở đây
    if hasattr(state, "winner"):
        return state.winner

    # fallback
    if state.current_player == "white":
        return "black"
    return "white"


def run_benchmark(num_games=50):
    results = {
        "AlphaBeta_win": 0,
        "MCTS_win": 0,
        "Draw": 0
    }

    for i in range(num_games):
        winner = play_one_game()

        if winner == "white":
            results["AlphaBeta_win"] += 1
        elif winner == "black":
            results["MCTS_win"] += 1
        else:
            results["Draw"] += 1

        print(f"Game {i+1}/{num_games} finished")

    return results


def save_csv(results, filename="match_result.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Result", "Count"])
        for k, v in results.items():
            writer.writerow([k, v])


if __name__ == "__main__":
    total = 5   # số trận muốn test
    stats = run_benchmark(total)

    print("\n===== FINAL RESULT =====")
    print(stats)

    save_csv(stats)
