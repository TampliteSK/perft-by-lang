# Board.py

from dataclass import dataclass
import datatypes

#define GET_RANK(sq) ((sq) / 8)
#define GET_FILE(sq) ((sq) % 8)
#define FR2SQ(f, r) ((r) * 8 + (f))

#define START_POS "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

@dataclass
class UndoBox:
    move: int
	castle_perms: int
	enpas: int
	fifty_move: int
    
class Board:
	pieces: list[int]  # Square -> Piece
	bitboards: list[datatypes.Bitboard]
	occupancies: list[datatypes.Bitboard]

	piece_num: list[int]
	king_sq: list[int]
	side: int
	enpas: int
	castle_perms: int
	fifty_move: int  # Counter for 50-move rule

	ply: int
	his_ply: int
	move_history: list[UndoBox]

	def __init__(self):
		self.reset_board()
	
	def reset_board(self):
		self.pieces = [datatypes.EMPTY] * 64
		self.bitboards = [0] * 13
#endif // BOARD_HPP