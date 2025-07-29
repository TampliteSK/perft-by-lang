// attackgen.h

#ifndef ATTACKGEN_H
#define ATTACKGEN_H

#include "datatypes.h"

// Attack tables
extern Bitboard pawn_attacks[2][64];     // pawn attacks table [side][square]
extern Bitboard knight_attacks[64];      // knight attacks table [square]
extern Bitboard king_attacks[64];        // king attacks table [square]
extern Bitboard bishop_masks[64];        // bishop attack masks
extern Bitboard rook_masks[64];          // rook attack masks
extern Bitboard bishop_attacks[64][512]; // bishop attacks table [square][occupancies]
extern Bitboard rook_attacks[64][4096];  // rook attacks table [square][occupancies]

// Functions
Bitboard mask_bishop_attacks(int sq);
Bitboard mask_rook_attacks(int sq);
Bitboard bishop_attacks_on_the_fly(int sq, Bitboard blockers);
Bitboard rook_attacks_on_the_fly(int sq, Bitboard blockers);

Bitboard get_bishop_attacks(int sq, Bitboard occupancy);
Bitboard get_rook_attacks(int sq, Bitboard occupancy);
Bitboard get_queen_attacks(int sq, Bitboard occupancy);

void init_leapers_attacks();
void init_sliders_attacks(int bishop);
Bitboard set_occupancy(int index, int bits_in_mask, Bitboard attack_mask);
void init_attack_tables();

enum { IS_BISHOP, IS_ROOK };

extern const int bishop_relevant_bits[64];
extern const int rook_relevant_bits[64];

extern const uint64_t bishop_magic_numbers[64];
extern const uint64_t rook_magic_numbers[64];

#endif // ATTACKGEN_H