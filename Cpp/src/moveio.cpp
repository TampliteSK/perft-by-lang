// moveio.cpp

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include "moveio.hpp"
#include "movegen.hpp"
#include "datatypes.hpp"

// print move (for UCI purposes)
std::string print_move(int move) {
    std::ostringstream oss;
    oss << ascii_squares[get_move_source(move)]
        << ascii_squares[get_move_target(move)];

    // Promoted pieces must be encoded in lowercase
    if (get_move_promoted(move)) {
        int promoted_piece = get_move_promoted(move);
        if (piece_type[promoted_piece] == QUEEN) {
            oss << "q";
        }
        else if (piece_type[promoted_piece] == ROOK) {
            oss << "r";
        }
        else if (piece_type[promoted_piece] == BISHOP) {
            oss << "b";
        }
        else if (piece_type[promoted_piece] == KNIGHT) {
            oss << "n";
        }
    }

    return oss.str();
}

void print_move_list(const MoveList move_list) {
    // Do nothing on empty move list
    if (move_list.length == 0) {
        std::cout << "\nMove list has no moves!\n";
        return;
    }

    std::cout << "Generated moves: \n";

    for (int move_count = 0; move_count < (int)move_list.length; move_count++) {
        int move = move_list.moves[move_count];
        std::cout << print_move(move) << " ";
        if (move_count % 5 == 4) {
            std::cout << "\n";
        }
    }

    // Print total number of moves
    std::cout << "\nCount: " << move_list.length << "\n\n";
}