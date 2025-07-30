# datatypes.py

from enum import Enum

MAX_DEPTH = 64
INF_BOUND = 30000
MAX_GAME_MOVES = 2048
MATE_SCORE = INF_BOUND - MAX_DEPTH

def CLAMP(value, min_value, max_value):
    return max(min_value, min(value, max_value))

"""
    Enums and Dicts
"""

# Piece enums
class Colour(Enum):
    WHITE = 0; BLACK = 1; BOTH = 2

class PType(Enum):
    NONE = 0
    PAWN = 1; KNIGHT = 2; BISHOP = 3; ROOK = 4; QUEEN = 5; KING = 6

class Piece(Enum):
    EMPTY = 0
    wP = 1; wN = 2; wB = 3; wR = 4; wQ = 5; wK = 6
    bP = 7; bN = 8; bB = 9; bR = 10; bQ = 11; bK = 12

ascii_pieces = ".PNBRQKpnbrqk"

# Mapping from Piece enum to PType enum
piece_type = {
    Piece.EMPTY: PType.NONE,
    Piece.wP: PType.PAWN, Piece.wN: PType.KNIGHT, Piece.wB: PType.BISHOP,
    Piece.wR: PType.ROOK, Piece.wQ:  PType.QUEEN, Piece.wK:   PType.KING,
    Piece.bP: PType.PAWN, Piece.bN: PType.KNIGHT, Piece.bB: PType.BISHOP,
    Piece.bR: PType.ROOK, Piece.bQ:  PType.QUEEN, Piece.bK:   PType.KING
}

# Mapping from Piece enum to Colour enum
piece_col = {
    Piece.EMPTY: Colour.BOTH,
    Piece.wP: Colour.WHITE, Piece.wN: Colour.WHITE, Piece.wB: Colour.WHITE,
    Piece.wR: Colour.WHITE, Piece.wQ: Colour.WHITE, Piece.wK: Colour.WHITE,
    Piece.bP: Colour.BLACK, Piece.bN: Colour.BLACK, Piece.bB: Colour.BLACK,
    Piece.bR: Colour.BLACK, Piece.bQ: Colour.BLACK, Piece.bK: Colour.BLACK
}

# Squares
class Squares(Enum):
    a8 = 0;  b8 = 1;  c8 = 2;  d8 = 3;  e8 = 4;  f8 = 5;  g8 = 6;  h8 = 7
    a7 = 8;  b7 = 9;  c7 = 10; d7 = 11; e7 = 12; f7 = 13; g7 = 14; h7 = 15
    a6 = 16; b6 = 17; c6 = 18; d6 = 19; e6 = 20; f6 = 21; g6 = 22; h6 = 23
    a5 = 24; b5 = 25; c5 = 26; d5 = 27; e5 = 28; f5 = 29; g5 = 30; h5 = 31
    a4 = 32; b4 = 33; c4 = 34; d4 = 35; e4 = 36; f4 = 37; g4 = 38; h4 = 39
    a3 = 40; b3 = 41; c3 = 42; d3 = 43; e3 = 44; f3 = 45; g3 = 46; h3 = 47
    a2 = 48; b2 = 49; c2 = 50; d2 = 51; e2 = 52; f2 = 53; g2 = 54; h2 = 55
    a1 = 56; b1 = 57; c1 = 58; d1 = 59; e1 = 60; f1 = 61; g1 = 62; h1 = 63
    NO_SQ = 64

Mirror64 = (
    56, 57, 58, 59, 60, 61, 62, 63,
    48, 49, 50, 51, 52, 53, 54, 55,
    40, 41, 42, 43, 44, 45, 46, 47,
    32, 33, 34, 35, 36, 37, 38, 39,
    24, 25, 26, 27, 28, 29, 30, 31,
    16, 17, 18, 19, 20, 21, 22, 23,
     8,  9, 10, 11, 12, 13, 14, 15,
     0,  1,  2,  3,  4,  5,  6,  7
)

# Mapping from Squares enum to ASCII representation
ascii_squares = (
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "NO_SQ"
)

# Files and Ranks
class Files(Enum):
    FILE_A = 0; FILE_B = 1; FILE_C = 2; FILE_D = 3; 
    FILE_E = 4; FILE_F = 5; FILE_G = 6; FILE_H = 7

class Ranks(Enum):
    RANK_8 = 0; RANK_7 = 1; RANK_6 = 2; RANK_5 = 3; 
    RANK_4 = 4; RANK_3 = 5; RANK_2 = 6; RANK_1 = 7

# Castling rights
class CastlingRights(Enum):
    WKCA = 1; WQCA = 2; BKCA = 4; BQCA = 8

    # Bitwise operations
    def __or__(self, other):
        if isinstance(other, CastlingRights):
            return CastlingRights(self.value | other.value)
        return NotImplemented

    def __xor__(self, other):
        if isinstance(other, CastlingRights):
            return CastlingRights(self.value ^ other.value)
        return NotImplemented

    def __and__(self, other):
        if isinstance(other, CastlingRights):
            return CastlingRights(self.value & other.value)
        return NotImplemented

    # In-place bitwise operations
    def __ior__(self, other):
        return self.__or__(other)

    def __ixor__(self, other):
        return self.__xor__(other)

    def __iand__(self, other):
        return self.__and__(other)