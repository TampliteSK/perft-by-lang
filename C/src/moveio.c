// moveio.c

#include "moveio.h"
#include "movegen.h"
#include "datatypes.h"

#include <stdio.h>

// print move (for UCI purposes)
char *print_move(const int move) {

	static char MvStr[6];

    int ff = GET_FILE(get_move_source(move));
    int rf = GET_RANK(get_move_source(move));
    int ft = GET_FILE(get_move_target(move));
    int rt = GET_RANK(get_move_target(move));
	int promoted = get_move_promoted(move);

	if (promoted) {
		char pchar = 'q';
		if (piece_type[promoted] == KNIGHT) {
			pchar = 'n';
		} else if (piece_type[promoted] == ROOK) {
			pchar = 'r';
		} else if (piece_type[promoted] == BISHOP) {
			pchar = 'b';
		}
		sprintf(MvStr, "%c%c%c%c%c", ('a'+ff), ('1'+rf), ('a'+ft), ('1'+rt), pchar);
	} else {
		sprintf(MvStr, "%c%c%c%c", ('a'+ff), ('1'+rf), ('a'+ft), ('1'+rt));
	}

	return MvStr;
}

void print_move_list(const MoveList move_list) {
    // Do nothing on empty move list
    if (move_list.length == 0) {
        printf("\nMove list has no moves!\n");
        return;
    }

    printf("Generated moves: \n");

    for (int move_count = 0; move_count < (int)move_list.length; move_count++) {
        int move = move_list.moves[move_count];
        printf("%s ", print_move(move));
        if (move_count % 5 == 4) {
            printf("\n");
        }
    }

    // Print total number of moves
    printf("\nCount: %d\n\n", move_list.length);
}