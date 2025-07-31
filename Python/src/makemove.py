# makemove.cpp

from makemove_helper import *
from Board import Board, UndoBox
from datatypes import Piece, PType, Squares, Colour, piece_col, piece_type
from Move import Move
from attack import is_square_attacked
from bitboard import *

# Functions based on VICE makemove.c by Richard Allbert
# Incrementally updating Board class move by move for better efficiency

"""
	Piece manipulation
"""

def clear_piece(pos: Board, sq: Squares) -> Board:
    pce = pos.pieces[sq.value]
    col = piece_col[pce]

    pos.pieces[sq.value] = Piece.EMPTY
    pos.piece_num[pce.value] -= 1

    pos.bitboards[pce.value] = clear_bit(pos.bitboards[pce.value], sq)
    pos.occupancies[col.value] = clear_bit(pos.occupancies[col.value], sq)
    pos.occupancies[Colour.BOTH.value] = clear_bit(pos.occupancies[Colour.BOTH.value], sq)
    return pos

def add_piece(pos: Board, sq: Squares, pce: Piece) -> Board:
	col = piece_col[pce]

	pos.pieces[sq.value] = pce
	pos.piece_num[pce.value] += 1

	pos.bitboards[pce.value] = set_bit(pos.bitboards[pce.value], sq)
	pos.occupancies[col.value] = set_bit(pos.occupancies[col.value], sq)
	pos.occupancies[Colour.BOTH.value] = set_bit(pos.occupancies[Colour.BOTH.value], sq)
	return pos

# "from" is a Python keyword, so we renamed it here
def move_piece(pos: Board, from_sq: Squares, to_sq: Squares) -> Board:
    pce = pos.pieces[from_sq.value]
    col = piece_col[pce]

    pos.pieces[from_sq.value] = Piece.EMPTY
    pos.bitboards[pce.value] = clear_bit(pos.bitboards[pce.value], from_sq)
    pos.occupancies[col.value] = clear_bit(pos.occupancies[col.value], from_sq)
    pos.occupancies[Colour.BOTH.value] = clear_bit(pos.occupancies[Colour.BOTH.value], from_sq)

    pos.pieces[to_sq.value] = pce
    pos.bitboards[pce.value] = set_bit(pos.bitboards[pce.value], to_sq)
    pos.occupancies[col.value] = set_bit(pos.occupancies[col.value], to_sq)
    pos.occupancies[Colour.BOTH.value] = set_bit(pos.occupancies[Colour.BOTH.value], to_sq)
    return pos

"""
	Move manipulation
"""

def take_move(pos: Board) -> Board:
    pos.ply -= 1
    pos.his_ply -= 1

    box = pos.move_history[pos.his_ply]
    move = box.move
    from_square = move.source
    to_square = move.target

    pos.castle_perms = box.castle_perms
    pos.fifty_move = box.fifty_move
    pos.enpas = box.enpas

    pos.side = Colour(pos.side.value ^ 1)

    if move.enpassant:
        # Recover the pawn that was enpassanted
        if pos.side == Colour.WHITE:
            pos = add_piece(pos, Squares(to_square.value + 8), Piece.bP)
        else:
            pos = add_piece(pos, Squares(to_square.value - 8), Piece.wP)
            
    elif move.castling:
        # Move the castling rook back
        if to_square == Squares.c1:
            pos = move_piece(pos, Squares.d1, Squares.a1)
        elif to_square == Squares.c8:
            pos = move_piece(pos, Squares.d8, Squares.a8)
        elif to_square == Squares.g1:
            pos = move_piece(pos, Squares.f1, Squares.h1)
        elif to_square == Squares.g8:
            pos = move_piece(pos, Squares.f8, Squares.h8)

    pos = move_piece(pos, to_square, from_square)

    if piece_type[pos.pieces[from_square.value]] == PType.KING:
        pos.king_sq[pos.side.value] = from_square

    # Undo captures
    captured = move.captured
    if captured != Piece.EMPTY and not move.enpassant:
        pos = add_piece(pos, to_square, captured)

    # Undo promotion
    if move.promoted != Piece.EMPTY:
        pos = clear_piece(pos, from_square)
        pos = add_piece(pos, from_square, Piece.wP if piece_col[move.promoted] == Colour.WHITE else Piece.bP)

    return pos

def make_move(pos: Board, move: Move) -> tuple[bool, Board]:
    from_square = move.source
    to_square = move.target
    side = pos.side

    box = UndoBox()

    if move.enpassant:
        # Clear the captured pawn
        if side == Colour.WHITE:
            pos = clear_piece(pos, Squares(to_square.value + 8))
        else:
            pos = clear_piece(pos, Squares(to_square.value - 8))
            
    elif move.castling:
        # Move the corresponding rook
        if to_square == Squares.c1:
            pos = move_piece(pos, Squares.a1, Squares.d1)
        elif to_square == Squares.c8:
            pos = move_piece(pos, Squares.a8, Squares.d8)
        elif to_square == Squares.g1:
            pos = move_piece(pos, Squares.h1, Squares.f1)
        elif to_square == Squares.g8:
            pos = move_piece(pos, Squares.h8, Squares.f8)

    box.move = move
    box.fifty_move = pos.fifty_move
    box.enpas = pos.enpas
    box.castle_perms = pos.castle_perms
    pos.move_history[pos.his_ply] = box

    pos.castle_perms &= castling_rights[from_square.value]
    pos.castle_perms &= castling_rights[to_square.value]
    pos.enpas = Squares.NO_SQ

    pos.fifty_move += 1

    # Handle captures
    captured = move.captured
    if captured:
        pos = clear_piece(pos, to_square)
        pos.fifty_move = 0  # A capture is played - reset 50-move counter

    pos.ply += 1
    pos.his_ply += 1

    if piece_type[pos.pieces[from_square.value]] == PType.PAWN:
        pos.fifty_move = 0  # A pawn is moved - reset 50-move counter
        # Check if it's a double advance
        if move.double_push:
            pos.enpas = Squares(from_square.value - 8) if side == Colour.WHITE else Squares(from_square.value + 8)

    pos = move_piece(pos, from_square, to_square)

    # Handle promotions
    prPce = move.promoted
    if prPce != Piece.EMPTY:
        # Replace the pawn with the promoted piece
        pos = clear_piece(pos, to_square)
        pos = add_piece(pos, to_square, prPce)

    # Detect king move
    if piece_type[pos.pieces[to_square.value]] == PType.KING:
        pos.king_sq[pos.side.value] = to_square

    # Switch sides
    pos.side = Colour(pos.side.value ^ 1)

    # It is an illegal move if we reveal a check to our king
    if is_square_attacked(pos, pos.king_sq[side.value], pos.side):
        pos = take_move(pos)
        return False, pos  # Illegal move

    return True, pos