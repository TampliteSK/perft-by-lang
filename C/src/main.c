// main.cpp

#include <stdio.h>
#include <stdlib.h> // For exit

#include "attackgen.h"
#include "Board.h"
#include "perft.h"

int main(int argc, char* argv[]) {
    init_attack_tables();

    Board* pos = (Board*)malloc(sizeof(Board));
    reset_board(pos);
    parse_fen(pos, START_POS);
    // print_board(pos);

    uint8_t perft_depth = 5;
    if (argc > 1) {
        int input = atoi(argv[1]);
        if (input < 1 || input > 10) {
            printf("Invalid depth. Please enter a value between 1 and 10.\n");
            free(pos);
            return EXIT_FAILURE;
        }
        perft_depth = atoi(argv[1]);
    }

    // Run performance test
    printf("Running perft with depth: %d\n", (int)perft_depth);
    run_perft(pos, perft_depth, TRUE);

    free(pos);
	return EXIT_SUCCESS;
}