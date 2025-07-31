# Board.py

from dataclasses import dataclass, field
from datatypes import Piece, Colour, Squares
from Move import Move
from typing import ClassVar
from bitboard import *

def GET_RANK(sq): return (sq) // 8
def GET_FILE(sq): return (sq) % 8
def FR2SQ(f, r): return (r) * 8 + (f)

START_POS = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

@dataclass
class UndoBox:
	move: Move = Move()
	castle_perms: int = 0
	enpas: ClassVar[Squares] = Squares.NO_SQ
	fifty_move: int = 0
	
class Board:
	pieces: list[Piece]  # Square -> Piece
	bitboards: list[Bitboard]
	occupancies: list[Bitboard]

	piece_num: list[int]
	king_sq: list[Squares]
	side: Colour
	enpas: Squares
	castle_perms: int
	fifty_move: int  # Counter for 50-move rule

	ply: int
	his_ply: int
	move_history: list[UndoBox]

	def __init__(self):
		self.reset_board()
	
	def reset_board(self):
		self.pieces = [Piece.EMPTY] * 64
		self.bitboards = [0 for _ in range(13)]
		self.occupancies = [0 for _ in range(3)]
		self.piece_num = [0] * 13
		self.king_sq = [Squares.NO_SQ] * 3
		self.side = Colour.WHITE
		self.enpas = Squares.NO_SQ
		self.castle_perms = 0
		self.fifty_move = 0
		self.ply = 0
		self.his_ply = 0
		self.move_history = [UndoBox() for _ in range(2048)]

	def update_vars(self):
		from datatypes import piece_type, piece_col, PType
		for pce in Piece:
			self.piece_num[pce.value] = count_bits(self.bitboards[pce.value])
			if piece_type[pce] == PType.KING:
				copy = self.bitboards[pce.value]
				sq, _ = pop_ls1b(copy)
				self.king_sq[piece_col[pce].value] = Squares(sq)

	def parse_fen(self, fen: str):
		from datatypes import Piece, piece_col
		self.reset_board()
		pfen = 0
		rank = 0
		file = 0
		piece = 0
		count = 0
		sq = 0
		fen = fen.strip()

		# Parse pieces
		while rank < 8 and pfen < len(fen):
			count = 1
			c = fen[pfen]
			if c == 'p':   piece = Piece.bP
			elif c == 'r': piece = Piece.bR
			elif c == 'n': piece = Piece.bN
			elif c == 'b': piece = Piece.bB
			elif c == 'k': piece = Piece.bK
			elif c == 'q': piece = Piece.bQ
			elif c == 'P': piece = Piece.wP
			elif c == 'R': piece = Piece.wR
			elif c == 'N': piece = Piece.wN
			elif c == 'B': piece = Piece.wB
			elif c == 'K': piece = Piece.wK
			elif c == 'Q': piece = Piece.wQ
			elif c in '12345678':
				piece = Piece.EMPTY
				count = int(c)
			elif c == '/':
				rank += 1
				file = 0
				pfen += 1
				continue
			elif c == ' ':
				pfen += 1
				break
			else:
				raise ValueError(f"Invalid FEN character: {c}")
			for _ in range(count):
				sq = rank * 8 + file
				if piece != Piece.EMPTY:
					self.pieces[sq] = piece
					self.bitboards[piece.value] = set_bit(self.bitboards[piece.value], Squares(sq))
					self.occupancies[Colour.BOTH.value] = set_bit(self.occupancies[Colour.BOTH.value], Squares(sq))
					self.occupancies[piece_col[piece].value] = set_bit(self.occupancies[piece_col[piece].value], Squares(sq))
				file += 1
			pfen += 1
		# Side to move
		if pfen < len(fen):
			self.side = Colour.WHITE if fen[pfen] == 'w' else Colour.BLACK
			pfen += 2
		# Castling rights
		for _ in range(4):
			if pfen >= len(fen) or fen[pfen] == ' ':
				break
			c = fen[pfen]
			if c == 'K': self.castle_perms |= 1
			elif c == 'Q': self.castle_perms |= 2
			elif c == 'k': self.castle_perms |= 4
			elif c == 'q': self.castle_perms |= 8
			pfen += 1
		if pfen < len(fen) and fen[pfen] == ' ':
			pfen += 1
		# En passant
		if pfen < len(fen) and fen[pfen] != '-':
			file = ord(fen[pfen]) - ord('a')
			rank = 8 - int(fen[pfen + 1])
			self.enpas = Squares(rank * 8 + file)
			pfen += 3
		else:
			self.enpas = Squares.NO_SQ
			pfen += 2

		# Fifty-move counter
		half_moves = ''
		while pfen < len(fen) and fen[pfen].isdigit():
			half_moves += fen[pfen]
			pfen += 1
		self.fifty_move = int(half_moves) if half_moves else 0
		if pfen < len(fen) and fen[pfen] == ' ':
			pfen += 1

		# Full move number (not stored)
		full_move = ''
		while pfen < len(fen) and fen[pfen].isdigit():
			full_move += fen[pfen]
			pfen += 1
		self.update_vars()


	def print_board(self):
		from datatypes import ascii_pieces
		print()
		for rank in range(8):
			print(f"  {8 - rank} ", end='')
			for file in range(8):
				sq = rank * 8 + file
				piece = self.pieces[sq]
				print(f" {ascii_pieces[piece.value]}", end='')
			print()
		print("\n     a b c d e f g h\n")
		print(f"           Side: {'White' if self.side == 0 else 'Black'}")
		print(f"     En passant: {self.enpas if self.enpas is not None else 'N/A'}")
		print(f"50-move counter: {self.fifty_move}")
		print(f"            Ply: {self.ply}")
		print(f"    History ply: {self.his_ply}")
		# Print castling rights
		cr = ''
		cr += 'K' if self.castle_perms & 1 else '-'
		cr += 'Q' if self.castle_perms & 2 else '-'
		cr += 'k' if self.castle_perms & 4 else '-'
		cr += 'q' if self.castle_perms & 8 else '-'
		print(f"       Castling: {cr}")