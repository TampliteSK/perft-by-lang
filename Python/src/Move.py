# Move.py

# Move encoding bit layout
"""
          binary move bits                               hexidecimal constants

    0000 0000 0000 0000 0000 0011 1111    source square       0x3f
    0000 0000 0000 0000 1111 1100 0000    target square       0xfc0
    0000 0000 0000 1111 0000 0000 0000    piece               0xf000
    0000 0000 1111 0000 0000 0000 0000    promoted piece      0xf0000
    0000 1111 0000 0000 0000 0000 0000    captured piece      0xf00000
    0001 0000 0000 0000 0000 0000 0000    double push flag    0x1000000
    0010 0000 0000 0000 0000 0000 0000    enpassant flag      0x2000000
    0100 0000 0000 0000 0000 0000 0000    castling flag       0x4000000
"""

class Move(int):
    @staticmethod
    def encode(source, target, piece, promoted, capture, double_adv, enpassant, castling):
        return Move(
            (source)
            | (target << 6)
            | (piece << 12)
            | (promoted << 16)
            | (capture << 20)
            | (double_adv << 24)
            | (enpassant << 25)
            | (castling << 26)
        )

    @property
    def source(self):
        # source: bits 0-5
        return self & 0x3f

    @property
    def target(self):
        # target: bits 6-11
        return (self & 0xfc0) >> 6

    @property
    def piece(self):
        # piece: bits 12-15
        return (self & 0xf000) >> 12

    @property
    def promoted(self):
        # promoted: bits 16-19
        return (self & 0xf0000) >> 16

    @property
    def captured(self):
        # captured: bits 20-23
        return (self & 0xf00000) >> 20

    @property
    def double_push(self):
        # double push: bit 24
        return bool(self & 0x1000000)

    @property
    def enpassant(self):
        # enpassant: bit 25
        return bool(self & 0x2000000)

    @property
    def castling(self):
        # castling: bit 26
        return bool(self & 0x4000000)

# MoveList class to hold a list of moves
class MoveList:
    def __init__(self):
        self.moves = []
        self.length = 0

    def add_move(self, move: Move):
        self.moves.append(move)
        self.length += 1

    def clear(self):
        self.moves.clear()
        self.length = 0

    def __getitem__(self, index):
        return self.moves[index]

    def __len__(self):
        return self.length