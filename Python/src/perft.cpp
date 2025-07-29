// perft.cpp

#include <iostream>
#include <cstdint>
#include <chrono>

#include "perft.hpp"
#include "Board.hpp"
#include "makemove.hpp"
#include "moveio.hpp"
#include "bitboard.hpp"
#include "attackgen.hpp"

// Get time in milliseconds
uint64_t get_time_ms() {
    auto now = std::chrono::steady_clock::now(); // Get the current time point
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()); // Convert to milliseconds since epoch
    return static_cast<uint64_t>(duration.count());
}

uint64_t run_perft(Board* pos, uint8_t depth, bool print_info) {
    if (depth == 0) {
        return 0;
    }

    uint64_t nodes = 0;
    uint64_t start = 0;

    MoveList move_list;
    init_move_list(move_list);
    generate_moves(pos, move_list, false);

    if (print_info) {
        std::cout << "\n     Performance test\n\n";
        start = get_time_ms();
    }

    for (int i = 0; i < (int)move_list.length; i++) {
        int curr_move = move_list.moves[i];

        // Skip illegal moves
        if (!make_move(pos, curr_move)) {
            continue;
        }

        uint64_t old_nodes = nodes;

        if (depth == 1) {
            nodes++;
        }
        else {
            nodes += run_perft(pos, depth - 1, false);
        }

        uint64_t new_nodes = nodes - old_nodes;

        take_move(pos);

        // Print move if root level
        if (print_info) {
            std::cout << print_move(curr_move) << ": " << new_nodes << "\n";
        }
    }

    // Print results if root level
    if (print_info) {
        uint64_t time = get_time_ms() - start;
        std::cout << "\n    Depth: " << (int)depth << "\n"
            << "    Nodes: " << nodes << "\n"
            << "     Time: " << time << "ms (" << (double)time / 1000 << "s)\n"
            << "      NPS: " << int(nodes / (double)time * 1000) << "\n\n";
    }

    return nodes;
}