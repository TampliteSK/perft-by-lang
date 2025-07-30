# Move.py

from datatypes import Piece, PType, Squares, ascii_squares, piece_type

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
    def encode(source: Squares, target: Squares, piece: Piece, 
               promoted: Piece, capture: Piece, 
               double_adv: int, enpassant: int, castling: int):
        return Move(
            (source.value)
            | (target.value << 6)
            | (piece.value << 12)
            | (promoted.value << 16)
            | (capture.value << 20)
            | (double_adv << 24)
            | (enpassant << 25)
            | (castling << 26)
        )

    @property
    def source(self):
        # source: bits 0-5
        source_index = self & 0x3f
        return Squares(source_index)

    @property
    def target(self):
        # target: bits 6-11
        target_index = (self & 0xfc0) >> 6
        return Squares(target_index)

    @property
    def piece(self):
        # piece: bits 12-15
        piece_index = (self & 0xf000) >> 12
        return Piece(piece_index)

    @property
    def promoted(self):
        # promoted: bits 16-19
        promoted_index = (self & 0xf0000) >> 16
        return Piece(promoted_index)

    @property
    def captured(self):
        # captured: bits 20-23
        captured_index = (self & 0xf00000)
        return Piece(captured_index)

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
    
    # Print the move with UCI format
    def print_move(self) -> str:
        move_str = f"{ascii_squares[self.source.value]}{ascii_squares[self.target.value]}"

        # Promoted pieces must be encoded in lowercase
        promoted_piece = self.promoted
        if promoted_piece:
            if piece_type[promoted_piece] == PType.QUEEN:
                move_str += "q"
            elif piece_type[promoted_piece] == PType.ROOK:
                move_str += "r"
            elif piece_type[promoted_piece] == PType.BISHOP:
                move_str += "b"
            elif piece_type[promoted_piece] == PType.KNIGHT:
                move_str += "n"

        return move_str

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
    
    def print_move_list(self) -> None:
        # Do nothing on empty move list
        if self.length == 0:
            print("\nMove list has no moves!")
            return

        print("Generated moves: ")

        for i, move in enumerate(self.moves):
            print(f"{move} ", end="")
            if i % 5 == 4:
                print()

        # Print total number of moves
        print(f"\nCount: {self.length}\n")