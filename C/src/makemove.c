// makemove.cpp

#include "makemove.h"
#include "Board.h"
#include "bitboard.h"
#include "movegen.h"
#include "attack.h"

// Functions based on VICE makemove.c by Richard Allbert
// Incrementally updating Board class move by move for better efficiency

// castling rights update constants
const int castling_rights[64] = {
     7, 15, 15, 15,  3, 15, 15, 11,
    15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15,
    13, 15, 15, 15, 12, 15, 15, 14
};

/*
	Piece manipulation
*/

static inline void clear_piece(Board *pos, const int sq) {
	int pce = pos->pieces[sq];
	int col = piece_col[pce];

	pos->pieces[sq] = EMPTY;
	pos->piece_num[pce]--;

	CLR_BIT(pos->bitboards[pce], sq);
	CLR_BIT(pos->occupancies[col], sq);
	CLR_BIT(pos->occupancies[BOTH], sq);
}

static void add_piece(Board *pos, const int sq, const int pce) {
	int col = piece_col[pce];

	pos->pieces[sq] = pce;
	pos->piece_num[pce]++;

	SET_BIT(pos->bitboards[pce], sq);
	SET_BIT(pos->occupancies[col], sq);
	SET_BIT(pos->occupancies[BOTH], sq);
}

static void move_piece(Board *pos, const int from, const int to) {
	int pce = pos->pieces[from];
	int col = piece_col[pce];

	pos->pieces[from] = EMPTY;
	CLR_BIT(pos->bitboards[pce], from);
	CLR_BIT(pos->occupancies[col], from);
	CLR_BIT(pos->occupancies[BOTH], from);

	pos->pieces[to] = pce;
	SET_BIT(pos->bitboards[pce], to);
	SET_BIT(pos->occupancies[col], to);
	SET_BIT(pos->occupancies[BOTH], to);
}

/*
	Move manipulation
*/

void take_move(Board *pos) {
	pos->ply--;
	pos->his_ply--;
	
	UndoBox box = pos->move_history[pos->his_ply];
	int move = box.move;
	int from = get_move_source(move);
	int to = get_move_target(move);

	pos->castle_perms = box.castle_perms;
	pos->fifty_move = box.fifty_move;
	pos->enpas = box.enpas;

	pos->side ^= 1;

	if (get_move_enpassant(move)) {
		// Recover the pawn that was enpassanted
		if (pos->side == WHITE) {
			add_piece(pos, to + 8, bP);
		}
		else {
			add_piece(pos, to - 8, wP);
		}
	}
	else if (get_move_castling(move)) {
		// Move the castling rook back
		switch (to) {
			case c1: move_piece(pos, d1, a1); break;
			case c8: move_piece(pos, d8, a8); break;
			case g1: move_piece(pos, f1, h1); break;
			case g8: move_piece(pos, f8, h8); break;
		}
	}

	move_piece(pos, to, from);

	if (piece_type[pos->pieces[from]] == KING) {
		pos->king_sq[pos->side] = from;
	}

	// Undo captures
	int captured = get_move_captured(move);
	if (captured != EMPTY && !get_move_enpassant(move)) {
		add_piece(pos, to, captured);
	}

	// Undo promotion
	if (get_move_promoted(move) != EMPTY) {
		clear_piece(pos, from);
		add_piece(pos, from, (piece_col[get_move_promoted(move)] == WHITE) ? wP : bP);
	}
}

// Makes a move on the board
// Returns true if legal, and false if illegal
bool make_move(Board* pos, int move) {
	int from = get_move_source(move);
	int to = get_move_target(move);
	int side = pos->side;

	UndoBox box = { 0, 0, 0, 0, 0 };

	if (get_move_enpassant(move)) {
		// Clear the captured pawn
		if (side == WHITE) {
			clear_piece(pos, to + 8);
		}
		else {
			clear_piece(pos, to - 8);
		}
	}
	else if (get_move_castling(move)) {
		// Move the corresponding rook
		switch (to) {
		case c1:
			move_piece(pos, a1, d1);
			break;
		case c8:
			move_piece(pos, a8, d8);
			break;
		case g1:
			move_piece(pos, h1, f1);
			break;
		case g8:
			move_piece(pos, h8, f8);
			break;
		}
	}

	box.move = move;
	box.fifty_move = pos->fifty_move;
	box.enpas = pos->enpas;
	box.castle_perms = pos->castle_perms;
	pos->move_history[pos->his_ply] = box;

	pos->castle_perms &= castling_rights[from];
	pos->castle_perms &= castling_rights[to];
	pos->enpas = NO_SQ;

	pos->fifty_move++;

	// Handle captures
	int captured = get_move_captured(move);
	if (captured) {
		clear_piece(pos, to);
		pos->fifty_move = 0; // A capture is played - reset 50-move counter
	}

	pos->ply++;
	pos->his_ply++;

	if (piece_type[pos->pieces[from]] == PAWN) {
		pos->fifty_move = 0; // A pawn is moved - reset 50-move counter
		// Check if it's double advance
		if (get_move_double(move)) {
			if (side == WHITE) {
				pos->enpas = from - 8;
			}
			else {
				pos->enpas = from + 8;
			}
		}
	}

	move_piece(pos, from, to);

	// Handle promotions
	int prPce = get_move_promoted(move);
	if (prPce != EMPTY) {
		// Replace the pawn with the promoted piece
		clear_piece(pos, to);
		add_piece(pos, to, prPce);
	}

	// Detect king move
	if (piece_type[pos->pieces[to]] == KING) {
		pos->king_sq[pos->side] = to;
	}

	// Switch sides
	pos->side ^= 1;

	// It is an illegal move if we reveal a check to our king
	// side: Our side (the mover)
	// pos->get_side(): Opponent's side (switched after making the move)
	if (is_square_attacked(pos, pos->king_sq[side], pos->side)) {
		take_move(pos);
		return FALSE; // Illegal move
	}

	return TRUE;
}