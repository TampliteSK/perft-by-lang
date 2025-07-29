// bitboard.hpp

#ifndef BITBOARD_HPP
#define BITBOARD_HPP

#include "datatypes.hpp"

// set/get/pop bit macros
#define GET_BIT(bitboard, square) ((bitboard) & (1ULL << (square)))
#define SET_BIT(bitboard, square) ((bitboard) |= (1ULL << (square)))
#define CLR_BIT(bitboard, square) ((bitboard) &= ~(1ULL << (square)))

// Bitboard functions
uint8_t pop_ls1b(Bitboard& bb);
uint8_t count_bits(Bitboard bb);
void print_bitboard(Bitboard board);

#endif // BITBOARD_HPP