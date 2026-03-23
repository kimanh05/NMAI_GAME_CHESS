class Move:
    def __init__(self, sr, sc, er, ec):
        self.sr = sr
        self.sc = sc
        self.er = er
        self.ec = ec

    def __repr__(self):
        return f"Move(({self.sr},{self.sc}) -> ({self.er},{self.ec}))"

    def __eq__(self, other):
        return (
            isinstance(other, Move)
            and self.sr == other.sr
            and self.sc == other.sc
            and self.er == other.er
            and self.ec == other.ec
        )