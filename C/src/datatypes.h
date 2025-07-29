// datatypes.hpp

#ifndef DATATYPES_H
#define DATATYPES_H

#include <stdint.h>

typedef uint8_t bool;
typedef unsigned long long Bitboard;

#define MAX_DEPTH 64
#define INF_BOUND 30000
#define MAX_GAME_MOVES 2048
#define MATE_SCORE (INF_BOUND - MAX_DEPTH)

#define CLAMP(value, min, max) ((value) < (min) ? (min) : ((value) > (max) ? (max) : (value)))

enum { FALSE, TRUE }; // Boolean values
enum { WHITE, BLACK, BOTH }; // Colour

// Pieces
enum { EMPTY, wP, wN, wB, wR, wQ, wK, bP, bN, bB, bR, bQ, bK };
enum { NONE, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING };
extern int piece_type[13];
extern int piece_col[13];

extern int Mirror64[64];

extern Bitboard file_masks[8];
extern Bitboard rank_masks[8];
extern Bitboard adjacent_files[8];
extern Bitboard passer_masks[8];

extern const char* ascii_pieces;

// Board
enum {
    a8 =  0, b8, c8, d8, e8, f8, g8, h8,
    a7 =  8, b7, c7, d7, e7, f7, g7, h7,
    a6 = 16, b6, c6, d6, e6, f6, g6, h6,
    a5 = 24, b5, c5, d5, e5, f5, g5, h5,
    a4 = 32, b4, c4, d4, e4, f4, g4, h4,
    a3 = 40, b3, c3, d3, e3, f3, g3, h3,
    a2 = 48, b2, c2, d2, e2, f2, g2, h2,
    a1 = 56, b1, c1, d1, e1, f1, g1, h1, NO_SQ = 64
};

extern const char* ascii_squares[65];

enum { FILE_A, FILE_B, FILE_C, FILE_D, FILE_E, FILE_F, FILE_G, FILE_H };
enum { RANK_8, RANK_7, RANK_6, RANK_5, RANK_4, RANK_3, RANK_2, RANK_1 };

enum { WKCA = 1, WQCA = 2, BKCA = 4, BQCA = 8 };

#endif // DATATYPES_H