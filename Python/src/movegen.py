# movegen.cpp

from Board import Board
from Move import Move, MoveList
from datatypes import Squares, Colour, Piece, CastlingRights, piece_col
from bitboard import *
from attackgen import pawn_attacks, knight_attacks, king_attacks, get_bishop_attacks, get_rook_attacks, get_queen_attacks
from attack import is_square_attacked, get_piece_attacks

# Add move to the move list
def add_move(move_list: MoveList, move: Move) -> MoveList:
    move_list.moves.append(move)
    move_list.length += 1
    return move_list

# Movegen function forked from BBC by Maksim Korzh (Code Monkey King)
def generate_moves(pos: Board, move_list: MoveList, noisy_only: bool) -> MoveList:
    source_square = Squares.NO_SQ
    target_square = Squares.NO_SQ
    side = pos.side
    col_offset = 0 if (side == Colour.WHITE) else 6

    bitboard = 0
    attacks = 0

    for piece_value in range(Piece.wP.value + col_offset, Piece.wK.value + col_offset + 1):
        piece = Piece(piece_value)
        # print(f"Generating moves for {piece} ({piece_value})")
        bitboard = pos.bitboards[piece_value]
        # print_bitboard(bitboard)

        # White pawns
        if piece == Piece.wP:
            while bitboard:
                source_square, bitboard = pop_ls1b(bitboard)
                target_square = Squares(source_square.value - 8)

                # Generate quiet pawn moves
                if not noisy_only:
                    if target_square.value >= Squares.a8.value and not get_bit(pos.occupancies[Colour.BOTH.value], Squares(target_square)):
                        # Pawn promotion
                        if Squares.a7.value <= source_square.value <= Squares.h7.value:
                            move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.wQ, Piece.EMPTY, 0, 0, 0))
                            move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.wR, Piece.EMPTY, 0, 0, 0))
                            move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.wB, Piece.EMPTY, 0, 0, 0))
                            move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.wN, Piece.EMPTY, 0, 0, 0))
                        else:
                            # One square ahead pawn move
                            move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.EMPTY, Piece.EMPTY, 0, 0, 0))

                            # Two squares ahead pawn move
                            if Squares.a2.value <= source_square.value <= Squares.h2.value and not get_bit(pos.occupancies[Colour.BOTH.value], Squares(target_square.value - 8)):
                                move_list = add_move(move_list, Move.encode(source_square, Squares(target_square.value - 8), piece, Piece.EMPTY, Piece.EMPTY, 1, 0, 0))

                attacks = pawn_attacks[side.value][source_square.value] & pos.occupancies[Colour.BLACK.value]
                attacks &= 0xFFFFFFFFFFFFFFFF  # Force to U64

                # Generate pawn captures
                while attacks:
                    target_square, attacks = pop_ls1b(attacks)
                    target_piece = pos.pieces[target_square.value]

                    # Pawn promotion
                    if Squares.a7.value <= source_square.value <= Squares.h7.value:
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.wQ, target_piece, 0, 0, 0))
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.wR, target_piece, 0, 0, 0))
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.wB, target_piece, 0, 0, 0))
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.wN, target_piece, 0, 0, 0))
                    else:
                        # Normal capture
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.EMPTY, target_piece, 0, 0, 0))

                # Generate en passant captures
                if pos.enpas != Squares.NO_SQ:
                    # Check if en passant is a valid capture
                    enpassant_attacks = pawn_attacks[side.value][source_square.value] & (1 << pos.enpas.value)
                    if enpassant_attacks:
                        target_enpassant, enpassant_attacks = pop_ls1b(enpassant_attacks)
                        move_list = add_move(move_list, Move.encode(source_square, target_enpassant, piece, Piece.EMPTY, Piece.bP, 0, 1, 0))

        # Black pawns
        elif piece == Piece.bP:
            while bitboard:
                source_square, bitboard = pop_ls1b(bitboard)
                target_square = Squares(source_square.value + 8)

                # Generate quiet pawn moves
                if not noisy_only:
                    if target_square.value <= Squares.h1.value and not get_bit(pos.occupancies[Colour.BOTH.value], Squares(target_square)):
                        # Pawn promotion
                        if Squares.a2.value <= source_square.value <= Squares.h2.value:
                            move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.bQ, Piece.EMPTY, 0, 0, 0))
                            move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.bR, Piece.EMPTY, 0, 0, 0))
                            move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.bB, Piece.EMPTY, 0, 0, 0))
                            move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.bN, Piece.EMPTY, 0, 0, 0))
                        else:
                            # One square ahead pawn move
                            move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.EMPTY, Piece.EMPTY, 0, 0, 0))

                            # Two squares ahead pawn move
                            if Squares.a7.value <= source_square.value <= Squares.h7.value and not get_bit(pos.occupancies[Colour.BOTH.value], Squares(target_square.value + 8)):
                                move_list = add_move(move_list, Move.encode(source_square, Squares(target_square.value + 8), piece, Piece.EMPTY, Piece.EMPTY, 1, 0, 0))

                attacks = pawn_attacks[side.value][source_square.value] & pos.occupancies[Colour.WHITE.value]
                attacks &= 0xFFFFFFFFFFFFFFFF  # Force to U64

                # Generate pawn captures
                while attacks:
                    target_square, attacks = pop_ls1b(attacks)
                    target_piece = pos.pieces[target_square.value]

                    # Pawn promotion
                    if Squares.a2.value <= source_square.value <= Squares.h2.value:
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.bQ, target_piece, 0, 0, 0))
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.bR, target_piece, 0, 0, 0))
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.bB, target_piece, 0, 0, 0))
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.bN, target_piece, 0, 0, 0))
                    else:
                        # Normal capture
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.EMPTY, target_piece, 0, 0, 0))

                # Generate en passant captures
                if pos.enpas != Squares.NO_SQ:
                    enpassant_attacks = pawn_attacks[side.value][source_square.value] & (1 << pos.enpas.value)
                    if enpassant_attacks:
                        target_enpassant, enpassant_attacks = pop_ls1b(enpassant_attacks)
                        move_list = add_move(move_list, Move.encode(source_square, target_enpassant, piece, Piece.EMPTY, Piece.wP, 0, 1, 0))

        # Everything else (Knights, Bishops, Rooks, Queens, Kings)
        else:
            # White castling moves
            if not noisy_only and piece == Piece.wK:
                # King side castling
                if pos.castle_perms & CastlingRights.WKCA.value:
                    if pos.pieces[Squares.f1.value] == Piece.EMPTY and pos.pieces[Squares.g1.value] == Piece.EMPTY:
                        if not is_square_attacked(pos, Squares.e1, Colour.BLACK) and not is_square_attacked(pos, Squares.f1, Colour.BLACK):
                            move_list = add_move(move_list, Move.encode(Squares.e1, Squares.g1, piece, Piece.EMPTY, Piece.EMPTY, 0, 0, 1))

                # Queen side castling
                if pos.castle_perms & CastlingRights.WQCA.value:
                    if pos.pieces[Squares.d1.value] == Piece.EMPTY and pos.pieces[Squares.c1.value] == Piece.EMPTY and pos.pieces[Squares.b1.value] == Piece.EMPTY:
                        if not is_square_attacked(pos, Squares.e1, Colour.BLACK) and not is_square_attacked(pos, Squares.d1, Colour.BLACK):
                            move_list = add_move(move_list, Move.encode(Squares.e1, Squares.c1, piece, Piece.EMPTY, Piece.EMPTY, 0, 0, 1))

            # Black castling moves
            elif not noisy_only and piece == Piece.bK:
                # King side castling
                if pos.castle_perms & CastlingRights.BKCA.value:
                    if pos.pieces[Squares.f8.value] == Piece.EMPTY and pos.pieces[Squares.g8.value] == Piece.EMPTY:
                        if not is_square_attacked(pos, Squares.e8, Colour.WHITE) and not is_square_attacked(pos, Squares.f8, Colour.WHITE):
                            move_list = add_move(move_list, Move.encode(Squares.e8, Squares.g8, piece, Piece.EMPTY, Piece.EMPTY, 0, 0, 1))

                # Queen side castling
                if pos.castle_perms & CastlingRights.BQCA.value:
                    if pos.pieces[Squares.d8.value] == Piece.EMPTY and pos.pieces[Squares.c8.value] == Piece.EMPTY and pos.pieces[Squares.b8.value] == Piece.EMPTY:
                        if not is_square_attacked(pos, Squares.e8, Colour.WHITE) and not is_square_attacked(pos, Squares.d8, Colour.WHITE):
                            move_list = add_move(move_list, Move.encode(Squares.e8, Squares.c8, piece, Piece.EMPTY, Piece.EMPTY, 0, 0, 1))

            while bitboard:
                source_square, bitboard = pop_ls1b(bitboard)
                attacks = get_piece_attacks(pos, piece, source_square) & (~pos.occupancies[Colour.WHITE.value] if side == Colour.WHITE else ~pos.occupancies[Colour.BLACK.value])
                attacks &= 0xFFFFFFFFFFFFFFFF  # force to U64

                while attacks:
                    target_square, attacks = pop_ls1b(attacks)
                    if target_square == Squares.NO_SQ:
                        print(f"Invalid square while popping attacks: {attacks}")

                    # Capture move
                    if piece_col[pos.pieces[target_square.value]] == (side.value ^ 1):
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.EMPTY, target_piece, 0, 0, 0))
                        # print(f"Add capture move {source_square} -> {target_square}")
                    # Quiet move
                    elif not noisy_only:
                        move_list = add_move(move_list, Move.encode(source_square, target_square, piece, Piece.EMPTY, Piece.EMPTY, 0, 0, 0))
                        # print(f"Add quiet move {source_square} -> {target_square}")

    return move_list