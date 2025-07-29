# attack.py

import attack
import attackgen
import Board
import bitboard
import movegen

# Check if the current square is attacked by a given side
def is_square_attacked(pos: Board.Board, sq: int, side: int) -> bool:
    # Pawns (flip the direction of the atacks)
    if ((side == WHITE) and (pawn_attacks[BLACK][sq] & pos->bitboards[wP])):
        return True
    if ((side == BLACK) and (pawn_attacks[WHITE][sq] & pos->bitboards[bP])):
        return True

    # Knights and Kings
    if (knight_attacks[sq] & ((side == WHITE) ? pos->bitboards[wN] : pos->bitboards[bN])) return True
    if (king_attacks[sq]   & ((side == WHITE) ? pos->bitboards[wK] : pos->bitboards[bK])) return True

    # Bishops, Rooks and Queens
    if (get_bishop_attacks(sq, pos->occupancies[BOTH]) & ((side == WHITE) ? pos->bitboards[wB] : pos->bitboards[bB])) return true;
    if (get_rook_attacks(sq, pos->occupancies[BOTH])   & ((side == WHITE) ? pos->bitboards[wR] : pos->bitboards[bR])) return true;
    if (get_queen_attacks(sq, pos->occupancies[BOTH])  & ((side == WHITE) ? pos->bitboards[wQ] : pos->bitboards[bQ])) return true;

    return False

Bitboard get_piece_attacks(const Board *pos, uint8_t pce, uint8_t sq) {
    if (piece_type[pce] ==   PAWN) return pawn_attacks[piece_col[pce]][sq];
    if (piece_type[pce] == KNIGHT) return knight_attacks[sq];
    if (piece_type[pce] == BISHOP) return get_bishop_attacks(sq, pos->occupancies[BOTH]);
    if (piece_type[pce] ==   ROOK) return get_rook_attacks(sq, pos->occupancies[BOTH]);
    if (piece_type[pce] ==  QUEEN) return get_queen_attacks(sq, pos->occupancies[BOTH]);
    if (piece_type[pce] ==   KING) return king_attacks[sq];
    return 0ULL;
}