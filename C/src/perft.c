// perft.c
#include "attackgen.h"
#include "bitboard.h"
#include "Board.h"
#include "datatypes.h"  
#include "makemove.h"
#include "movegen.h"
#include "moveio.h"
#include "perft.h"

#include <stdint.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>

// Get time in milliseconds
uint64_t get_time_ms() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)(ts.tv_sec * 1000 + ts.tv_nsec / 1000000);
}

uint64_t run_perft(Board* pos, uint8_t depth, bool print_info) {
    if (depth == 0) {
        return 0;
    }

    uint64_t nodes = 0;
    uint64_t start = 0;

    MoveList* move_list = (MoveList*)malloc(sizeof(MoveList));
    init_move_list(move_list);
    generate_moves(pos, move_list, FALSE);

    if (print_info) {
        printf("\n     Performance test\n\n");
        start = get_time_ms();
    }

    for (int i = 0; i < (int)move_list->length; i++) {
        int curr_move = move_list->moves[i];

        // Skip illegal moves
        if (!make_move(pos, curr_move)) {
            continue;
        }

        uint64_t old_nodes = nodes;

        if (depth == 1) {
            nodes++;
        }
        else {
            nodes += run_perft(pos, depth - 1, FALSE);
        }

        uint64_t new_nodes = nodes - old_nodes;

        take_move(pos);

        // Print move if root level
        if (print_info) {
            printf("%s: %llu\n", print_move(curr_move), new_nodes);
        }
    }

    // Print results if root level
    if (print_info) {
        uint64_t time = get_time_ms() - start;
        printf("\n    Depth: %d\n"
               "    Nodes: %llu\n"
               "     Time: %llums (%.2fs)\n"
               "      NPS: %d\n\n",
               depth, nodes, time, (double)time / 1000, (int)(nodes / (double)time * 1000));
    }

    return nodes;
}