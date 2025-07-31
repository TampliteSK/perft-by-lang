# attack.py

from datatypes import piece_type, piece_col, Piece, Squares, Colour, PType
from Board import Board
from bitboard import Bitboard
from attackgen import pawn_attacks, knight_attacks, king_attacks, get_bishop_attacks, get_rook_attacks, get_queen_attacks

# Check if the current square is attacked by a given side
def is_square_attacked(pos: Board, sq: Squares, side: Colour) -> bool:
    # Pawns (flip the direction of the atacks)
    if ((side == Colour.WHITE) and (pawn_attacks[Colour.BLACK.value][sq.value] & pos.bitboards[Piece.wP.value])):
        return True
    if ((side == Colour.BLACK) and (pawn_attacks[Colour.WHITE.value][sq.value] & pos.bitboards[Piece.bP.value])):
        return True

    # Knights and Kings
    if (knight_attacks[sq.value] & (pos.bitboards[Piece.wN.value] if (side == Colour.WHITE) else pos.bitboards[Piece.bN.value])): return True
    if (king_attacks[sq.value]   & (pos.bitboards[Piece.wK.value] if (side == Colour.WHITE) else pos.bitboards[Piece.bK.value])): return True

    # Bishops, Rooks and Queens
    if (get_bishop_attacks(sq, pos.occupancies[Colour.BOTH.value]) & (pos.bitboards[Piece.wB.value] if (side == Colour.WHITE) else pos.bitboards[Piece.bB.value])): return True
    if (get_rook_attacks(sq, pos.occupancies[Colour.BOTH.value])   & (pos.bitboards[Piece.wR.value] if (side == Colour.WHITE) else pos.bitboards[Piece.bR.value])): return True
    if (get_queen_attacks(sq, pos.occupancies[Colour.BOTH.value])  & (pos.bitboards[Piece.wQ.value] if (side == Colour.WHITE) else pos.bitboards[Piece.bQ.value])): return True

    return False

def get_piece_attacks(pos: Board, pce: Piece, sq: Squares) -> Bitboard:
    if (piece_type[pce] ==   PType.PAWN): return pawn_attacks[piece_col[pce].value][sq.value]
    if (piece_type[pce] == PType.KNIGHT): return knight_attacks[sq.value]
    if (piece_type[pce] == PType.BISHOP): return get_bishop_attacks(sq, pos.occupancies[Colour.BOTH.value])
    if (piece_type[pce] ==   PType.ROOK): return get_rook_attacks(sq, pos.occupancies[Colour.BOTH.value])
    if (piece_type[pce] ==  PType.QUEEN): return get_queen_attacks(sq, pos.occupancies[Colour.BOTH.value])
    if (piece_type[pce] ==   PType.KING): return king_attacks[sq.value]
    return 0