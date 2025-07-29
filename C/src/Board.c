// Board.c

#include "datatypes.h"
#include "movegen.h"
#include "Board.h"
#include "bitboard.h"
#include "moveio.h"

#include <stdio.h>
#include <stdlib.h> // atoi()
#include <string.h> // strlen()

/*
	Macro board manipulation
*/

void reset_board(Board* pos) {

	for (int sq = 0; sq < 64; ++sq) {
		pos->pieces[sq] = EMPTY;
	}

	for (int i = 0; i < 13; ++i) {
		pos->bitboards[i] = 0ULL;
		pos->piece_num[i] = 0;
		if (i < 3) {
			pos->occupancies[i] = 0ULL;
			pos->king_sq[i] = NO_SQ;
		}
	}

	pos->side = WHITE;
	pos->enpas = NO_SQ;
	pos->castle_perms = 0;
	pos->fifty_move = 0;
	pos->ply = 0;
	pos->his_ply = 0;

	for (int i = 0; i < 2048; ++i) {
		UndoBox box = pos->move_history[i];
		box.castle_perms = 0;
		box.enpas = 0;
		box.fifty_move = 0;
		box.hash_key = 0ULL;
		box.move = 0; // NO_MOVE
		pos->move_history[i] = box;
	}
}

// Update other variables of the board, for when only bitboards and occupancies were setup
void update_vars(Board* pos) {
	for (int pce = wP; pce <= bK; ++pce) {
		pos->piece_num[pce] = count_bits(pos->bitboards[pce]);
		if (piece_type[pce] == KING) {
			Bitboard copy = pos->bitboards[pce];
			pos->king_sq[piece_col[pce]] = pop_ls1b(&copy);
		}
	}
}

// Rewritten from VICE parse_fen() function by Richard Allbert
void parse_fen(Board* pos, const char* FEN) {

	if (strlen(FEN) <= 0) {
		printf("Board parse_fen() error: Invalid FEN length.\n");
	}

	reset_board(pos);
	int pfen = 0; // Pointer to FEN character.

	/********************
	**  Parsing Pieces **
	****************** */

	int rank  = RANK_8;
	int file  = FILE_A;
	int piece = 0;
	int count = 0; // no. of consecutive empty squares / placeholder
	int sq    = 0;

	while ((rank <= RANK_1) && pfen < (int)strlen(FEN)) {
		count = 1;

		switch (FEN[pfen]) {
			case 'p': piece = bP; break;
			case 'r': piece = bR; break;
			case 'n': piece = bN; break;
			case 'b': piece = bB; break;
			case 'k': piece = bK; break;
			case 'q': piece = bQ; break;
			case 'P': piece = wP; break;
			case 'R': piece = wR; break;
			case 'N': piece = wN; break;
			case 'B': piece = wB; break;
			case 'K': piece = wK; break;
			case 'Q': piece = wQ; break;

			case '1':
			case '2':
			case '3':
			case '4':
			case '5':
			case '6':
			case '7':
			case '8':
				piece = EMPTY;
				count = FEN[pfen] - '0'; // number of consecutive empty squares
				break;

			case '/':
			case ' ':
				rank++;
				file = FILE_A;
				pfen++;
				continue;

			default:
				printf("Board parse_fen() error: Invalid FEN character: %c\n", FEN[pfen]);
				return;
		}

		// Putting pieces on the board
		for (int i = 0; i < count; i++) {
			sq = FR2SQ(file, rank);
			// Skips a file if empty square
			if (piece != EMPTY) { 
				pos->pieces[sq] = piece;
				SET_BIT(pos->bitboards[piece], sq);
				SET_BIT(pos->occupancies[BOTH], sq);
				SET_BIT(pos->occupancies[piece_col[piece]], sq);
			}
			file++;
		}
		pfen++;
	}

	/********************
	* Parsing Misc Data *
	****************** */

	// Side-to-move parsing
	pos->side = (FEN[pfen] == 'w') ? WHITE : BLACK;
	pfen += 2;

	// Castling perm parsing
	for (int i = 0; i < 4; i++) {
		if (FEN[pfen] == ' ') {
			break;
		}
		switch (FEN[pfen]) {
			case 'K': pos->castle_perms |= WKCA; break;
			case 'Q': pos->castle_perms |= WQCA; break;
			case 'k': pos->castle_perms |= BKCA; break;
			case 'q': pos->castle_perms |= BQCA; break;
			default: break;
		}
		pfen++;
	}
	pfen++;

	// En passant parsing
	if (FEN[pfen] != '-') {
		file = FEN[pfen]     - 'a';
		rank = 8 - (int)(FEN[pfen + 1] - '1');
		pos->enpas = FR2SQ(file, rank);
		pfen += 3;
	}
	else {
		pfen += 2;
	}

	// Fifty-move counter parsing
	uint16_t half_moves = 0;
	while (pfen < (int)strlen(FEN) && FEN[pfen] != ' ') {
		half_moves = half_moves * 10 + (FEN[pfen] - '0');
		pfen++;
	}
	pos->fifty_move = half_moves;
	pfen++; // Move past the space

	// Full move number parsing
	uint16_t full_move = 0;
	while (pfen < (int)strlen(FEN)) {
		if (FEN[pfen] == ' ') {
			break;
		}
		full_move = full_move * 10 + (FEN[pfen] - '0');
		pfen++;
	}

	update_vars(pos);
}

/*
	Output functions (debug)
*/

void print_board(const Board* pos) {
	printf("\n");

	for (int rank = RANK_8; rank <= RANK_1; rank++) {
		for (int file = FILE_A; file <= FILE_H; file++) {
			if (file == 0)
				printf("  %d ", 8 - rank); // Print rank number

			uint8_t sq = FR2SQ(file, rank);
			int piece = pos->pieces[sq];
			printf(" %c", ascii_pieces[piece]);
		}
		printf("\n");
	}

	printf("\n     a b c d e f g h\n\n");
	printf("           Side: %s\n", (pos->side == 0 ? "White" : "Black"));
	if (pos->enpas != NO_SQ)
		printf("     En passant: %s\n", ascii_squares[pos->enpas]);
	else
		printf("     En passant: N/A\n");
	printf("50-move counter: %d\n", (int)pos->fifty_move);
	printf("            Ply: %d\n", (int)pos->ply);
	printf("    History ply: %d\n", (int)pos->his_ply);

	// Print castling rights
	printf("       Castling: %c%c%c%c\n",
		(pos->castle_perms & WKCA) ? 'K' : '-',
		(pos->castle_perms & WQCA) ? 'Q' : '-',
		(pos->castle_perms & BKCA) ? 'k' : '-',
		(pos->castle_perms & BQCA) ? 'q' : '-');
}