// bitboard.cpp

#include "datatypes.hpp"
#include "bitboard.hpp"
#include "Board.hpp"

#include <bit>
#include <bitset>
#include <cstdint>
#include <iostream>

/*
    Bit Manipulation
*/

// Clears the least significant set bit and returns its index (0 - 63)
uint8_t pop_ls1b(Bitboard& bb) {
    uint8_t index = __builtin_ctzll(bb); // Use gcc/clang intrinsic
    bb &= ~1ULL << index;
    return index;
}

// Counts the number of set bits in a bitboard
uint8_t count_bits(Bitboard bb) {
    return (uint8_t)std::popcount(bb);
}

/*
    Misc
*/

void print_bitboard(Bitboard board) {

    std::cout << "\n";

    for (int rank = RANK_8; rank <= RANK_1; ++rank) {
        std::cout << 8 - rank << "   ";
        for (int file = FILE_A; file <= FILE_H; ++file) {
            uint8_t sq = FR2SQ(file, rank);
            if (GET_BIT(board, sq)) {
                std::cout << "X";
            }
            else {
                std::cout << "-";
            }
        }
        std::cout << "\n";
    }

    std::cout << "    ABCDEFGH\n\n";
    std::cout << "Bits set: " << (int)count_bits(board) << "\n";
    std::cout << "\n";
}