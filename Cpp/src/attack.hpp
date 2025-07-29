// attack.hpp

#ifndef ATTACK_HPP
#define ATTACK_HPP

#include "Board.hpp"
#include <cstdint>

bool is_square_attacked(const Board *pos, uint8_t sq, uint8_t side);
Bitboard get_piece_attacks(const Board* pos, uint8_t pce, uint8_t sq);

#endif // ATTACK_HPP