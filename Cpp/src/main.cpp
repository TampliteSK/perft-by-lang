// main.cpp

#include <iostream>
#include <cstdlib> // For exit

#include "attackgen.hpp"
#include "Board.hpp"
#include "perft.hpp"

int main(int argc, char* argv[]) {
    init_attack_tables();

    Board* pos = (Board*)malloc(sizeof(Board));
    reset_board(pos);
    parse_fen(pos, START_POS);
    // print_board(pos);

    uint8_t perft_depth = 5;
    if (argc > 1) {
        int input = std::atoi(argv[1]);
        if (input < 1 || input > 10) {
            std::cerr << "Invalid depth. Please enter a value between 1 and 10." << std::endl;
            free(pos);
            return EXIT_FAILURE;
        }
        perft_depth = std::atoi(argv[1]);
    }

    // Run performance test
    std::cout << "Running perft with depth: " << (int)perft_depth << std::endl;
    run_perft(pos, perft_depth, true);

    free(pos);
	return EXIT_SUCCESS;
}