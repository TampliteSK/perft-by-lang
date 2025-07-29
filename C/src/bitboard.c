// bitboard.c

#include "datatypes.h"
#include "bitboard.h"
#include "Board.h"

#include <stdint.h>
#include <stdio.h>

/*
    Bit Manipulation
*/

// Clears the least significant set bit and returns its index (0 - 63)
uint8_t pop_ls1b(Bitboard* bb) {
    uint8_t index = __builtin_ctzll(*bb); // Use gcc/clang intrinsic
    *bb &= ~1ULL << index;
    return index;
}

// Counts the number of set bits in a bitboard
uint8_t count_bits(Bitboard bb) {
    return __builtin_popcountll(bb);
}

/*
    Misc
*/

void print_bitboard(Bitboard board) {

    printf("\n");

    for (int rank = RANK_8; rank <= RANK_1; ++rank) {
        printf("%d   ", 8 - rank);
        for (int file = FILE_A; file <= FILE_H; ++file) {
            uint8_t sq = FR2SQ(file, rank);
            if (GET_BIT(board, sq)) {
                printf("X");
            }
            else {
                printf("-");
            }
        }
        printf("\n");
    }

    printf("  ABCDEFGH\n\n");
    printf("Bits set: %d\n", (int)count_bits(board));
    printf("\n");
}