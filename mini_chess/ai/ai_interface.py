class BaseAI:
    def choose_move(self, state):
        raise NotImplementedError("AI must implement choose_move(state)")