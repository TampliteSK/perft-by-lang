// attack.cpp

#include "attack.hpp"
#include "attackgen.hpp"
#include "Board.hpp"
#include "bitboard.hpp"
#include "movegen.hpp"

// Check if the current square is attacked by a given side
bool is_square_attacked(const Board *pos, uint8_t sq, uint8_t side) {

    // Pawns (flip the direction of the atacks)
    if ((side == WHITE) && (pawn_attacks[BLACK][sq] & pos->bitboards[wP])) return true;
    if ((side == BLACK) && (pawn_attacks[WHITE][sq] & pos->bitboards[bP])) return true;

    // Knights and Kings
    if (knight_attacks[sq] & ((side == WHITE) ? pos->bitboards[wN] : pos->bitboards[bN])) return true;
    if (king_attacks[sq]   & ((side == WHITE) ? pos->bitboards[wK] : pos->bitboards[bK])) return true;

    // Bishops, Rooks and Queens
    if (get_bishop_attacks(sq, pos->occupancies[BOTH]) & ((side == WHITE) ? pos->bitboards[wB] : pos->bitboards[bB])) return true;
    if (get_rook_attacks(sq, pos->occupancies[BOTH])   & ((side == WHITE) ? pos->bitboards[wR] : pos->bitboards[bR])) return true;
    if (get_queen_attacks(sq, pos->occupancies[BOTH])  & ((side == WHITE) ? pos->bitboards[wQ] : pos->bitboards[bQ])) return true;

    return false;
}

Bitboard get_piece_attacks(const Board *pos, uint8_t pce, uint8_t sq) {
    if (piece_type[pce] ==   PAWN) return pawn_attacks[piece_col[pce]][sq];
    if (piece_type[pce] == KNIGHT) return knight_attacks[sq];
    if (piece_type[pce] == BISHOP) return get_bishop_attacks(sq, pos->occupancies[BOTH]);
    if (piece_type[pce] ==   ROOK) return get_rook_attacks(sq, pos->occupancies[BOTH]);
    if (piece_type[pce] ==  QUEEN) return get_queen_attacks(sq, pos->occupancies[BOTH]);
    if (piece_type[pce] ==   KING) return king_attacks[sq];
    return 0ULL;
}