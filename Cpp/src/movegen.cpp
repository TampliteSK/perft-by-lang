// movegen.cpp

#include <vector>
#include <cstdint>
#include <iostream>
#include <algorithm>
#include "movegen.hpp"
#include "attack.hpp"
#include "attackgen.hpp"
#include "bitboard.hpp"
#include "makemove.hpp"

void init_move_list(MoveList& move_list) {
    for (int i = 0; i < MAX_LEGAL_MOVES; i++) {
        move_list.moves[i] = NO_MOVE;
    }
    move_list.length = 0;
}

// add move to the move list
static inline void add_move(MoveList& move_list, int move) {
    move_list.moves[move_list.length] = move;
    move_list.length++;
}

// Movegen function forked from BBC by Maksim Korzh (Code Monkey King)
void generate_moves(const Board *pos, MoveList& move_list, bool noisy_only) {

    uint8_t source_square, target_square;
    uint8_t side = pos->side;
    uint8_t col_offset = (side == WHITE) ? 0 : 6;
    Bitboard bitboard, attacks; // define current piece's bitboard copy & it's attacks

    for (int piece = wP + col_offset; piece <= wK + col_offset; piece++) {
        bitboard = pos->bitboards[piece];

        // White pawns
        if (piece == wP) {
            // loop over white pawns within white pawn bitboard
            while (bitboard) {
                source_square = pop_ls1b(bitboard);
                target_square = source_square - 8;

                // Generate quiet pawn moves
                if (!noisy_only) {
                    if (target_square >= a8 && !GET_BIT(pos->occupancies[BOTH], target_square)) {

                        // pawn promotion
                        if (source_square >= a7 && source_square <= h7) {
                            add_move(move_list, encode_move(source_square, target_square, piece, wQ, 0, 0, 0, 0));
                            add_move(move_list, encode_move(source_square, target_square, piece, wR, 0, 0, 0, 0));
                            add_move(move_list, encode_move(source_square, target_square, piece, wB, 0, 0, 0, 0));
                            add_move(move_list, encode_move(source_square, target_square, piece, wN, 0, 0, 0, 0));
                        }
                        else {
                            // one square ahead pawn move
                            add_move(move_list, encode_move(source_square, target_square, piece, 0, 0, 0, 0, 0));

                            // two squares ahead pawn move
                            if (source_square >= a2 && source_square <= h2 && !GET_BIT(pos->occupancies[BOTH], target_square - 8)) {
                                add_move(move_list, encode_move(source_square, target_square - 8, piece, 0, 0, 1, 0, 0));
                            }
                        }
                    }
                }

                attacks = pawn_attacks[side][source_square] & pos->occupancies[BLACK];

                // generate pawn captures
                while (attacks) {

                    target_square = pop_ls1b(attacks);
                    int target_pce = pos->pieces[target_square];

                    // pawn promotion
                    if (source_square >= a7 && source_square <= h7) {
                        add_move(move_list, encode_move(source_square, target_square, piece, wQ, target_pce, 0, 0, 0));
                        add_move(move_list, encode_move(source_square, target_square, piece, wR, target_pce, 0, 0, 0));
                        add_move(move_list, encode_move(source_square, target_square, piece, wB, target_pce, 0, 0, 0));
                        add_move(move_list, encode_move(source_square, target_square, piece, wN, target_pce, 0, 0, 0));
                    }
                    else {
                        // Normal capture
                        add_move(move_list, encode_move(source_square, target_square, piece, 0, target_pce, 0, 0, 0));
                    }
                }

                // generate enpassant captures
                if (pos->enpas != NO_SQ) {
                    Bitboard enpassant_attacks = pawn_attacks[side][source_square] & (1ULL << pos->enpas); // Check if enpassant is a valid capture
                    if (enpassant_attacks) {
                        int target_enpassant = pop_ls1b(enpassant_attacks);
                        add_move(move_list, encode_move(source_square, target_enpassant, piece, 0, bP, 0, 1, 0));
                    }
                }
            }
        }

        // Black pawn moves
        else if (piece == bP) {
            while (bitboard) {
                source_square = pop_ls1b(bitboard);
                target_square = source_square + 8;

                // Generate quiet pawn moves
                if (!noisy_only) {
                    if (target_square <= h1 && !GET_BIT(pos->occupancies[BOTH], target_square)) {

                        // pawn promotion
                        if (source_square >= a2 && source_square <= h2) {
                            add_move(move_list, encode_move(source_square, target_square, piece, bQ, 0, 0, 0, 0));
                            add_move(move_list, encode_move(source_square, target_square, piece, bR, 0, 0, 0, 0));
                            add_move(move_list, encode_move(source_square, target_square, piece, bB, 0, 0, 0, 0));
                            add_move(move_list, encode_move(source_square, target_square, piece, bN, 0, 0, 0, 0));
                        }
                        else {
                            // one square ahead pawn move
                            add_move(move_list, encode_move(source_square, target_square, piece, 0, 0, 0, 0, 0));

                            // two squares ahead pawn move
                            if (source_square >= a7 && source_square <= h7 && !GET_BIT(pos->occupancies[BOTH], target_square + 8)) {
                                add_move(move_list, encode_move(source_square, target_square + 8, piece, 0, 0, 1, 0, 0));
                            }

                        }
                    }
                }

                attacks = pawn_attacks[side][source_square] & pos->occupancies[WHITE];

                // generate pawn captures
                while (attacks) {

                    target_square = pop_ls1b(attacks);
                    int target_pce = pos->pieces[target_square];

                    // pawn promotion
                    if (source_square >= a2 && source_square <= h2) {
                        add_move(move_list, encode_move(source_square, target_square, piece, bQ, target_pce, 0, 0, 0));
                        add_move(move_list, encode_move(source_square, target_square, piece, bR, target_pce, 0, 0, 0));
                        add_move(move_list, encode_move(source_square, target_square, piece, bB, target_pce, 0, 0, 0));
                        add_move(move_list, encode_move(source_square, target_square, piece, bN, target_pce, 0, 0, 0));
                    }
                    else {
                        // Normal capture
                        add_move(move_list, encode_move(source_square, target_square, piece, 0, target_pce, 0, 0, 0));
                    }
                }

                // generate enpassant captures
                if (pos->enpas != NO_SQ) {
                    Bitboard enpassant_attacks = pawn_attacks[side][source_square] & (1ULL << pos->enpas);
                    if (enpassant_attacks) {
                        int target_enpassant = pop_ls1b(enpassant_attacks);
                        add_move(move_list, encode_move(source_square, target_enpassant, piece, 0, wP, 0, 1, 0));
                    }
                }
            }
        }

        // Everything else
        else {
            // White castling moves
            if (!noisy_only && piece == wK) {
                // King side castling
                if (pos->castle_perms & WKCA) {
                    if (pos->pieces[f1] == EMPTY && pos->pieces[g1] == EMPTY) {
                        if (!is_square_attacked(pos, e1, BLACK) && !is_square_attacked(pos, f1, BLACK)) {
                            add_move(move_list, encode_move(e1, g1, piece, 0, 0, 0, 0, 1));
                        }
                    }
                }
                // Queen side castling
                if (pos->castle_perms & WQCA) {
                    if (pos->pieces[d1] == EMPTY && pos->pieces[c1] == EMPTY && pos->pieces[b1] == EMPTY) {
                        if (!is_square_attacked(pos, e1, BLACK) && !is_square_attacked(pos, d1, BLACK)) {
                            add_move(move_list, encode_move(e1, c1, piece, 0, 0, 0, 0, 1));
                        }
                    }
                }
            }
            // Black castling moves
            else if (!noisy_only && piece == bK) {
                // King side castling
                if (pos->castle_perms & BKCA) {
                    if (pos->pieces[f8] == EMPTY && pos->pieces[g8] == EMPTY) {
                        if (!is_square_attacked(pos, e8, WHITE) && !is_square_attacked(pos, f8, WHITE)) {
                            add_move(move_list, encode_move(e8, g8, piece, 0, 0, 0, 0, 1));
                        }
                    }
                }
                // Queen side castling
                if (pos->castle_perms & BQCA) {
                    if (pos->pieces[d8] == EMPTY && pos->pieces[c8] == EMPTY && pos->pieces[b8] == EMPTY) {
                        if (!is_square_attacked(pos, e8, WHITE) && !is_square_attacked(pos, d8, WHITE)) {
                            add_move(move_list, encode_move(e8, c8, piece, 0, 0, 0, 0, 1));
                        }
                    }
                }
            }
            
            while (bitboard) {
                source_square = pop_ls1b(bitboard);
                attacks = get_piece_attacks(pos, piece, source_square) & ((side == WHITE) ? ~pos->occupancies[WHITE] : ~pos->occupancies[BLACK]);

                while (attacks) {
                    target_square = pop_ls1b(attacks);
                    int target_pce = pos->pieces[target_square];

                    // Capture move
                    if (piece_col[pos->pieces[target_square]] == (side ^ 1)) {
                        add_move(move_list, encode_move(source_square, target_square, piece, 0, target_pce, 0, 0, 0));
                    }
                    // Quiet move
                    else if (!noisy_only) {
                        add_move(move_list, encode_move(source_square, target_square, piece, 0, 0, 0, 0, 0));
                    }
                }
            }
        }
    }
}