# main.py

import attackgen
import Board
import perft

def main(argc: int, argv: list):
    attackgen.init_attack_tables()

    pos = Board.Board()
    pos.reset_board()
    pos.parse_fen(Board.START_POS)
    # print_board(pos);

    perft_depth = 5
    if (argc > 1):
        input = int(argv[1])
        if (input < 1 or input > 10) {
            print("Invalid depth. Please enter a value between 1 and 10.")
            return;
        }
        perft_depth = int(argv[1])

    # Run performance test
    print(f"Running perft with depth: {perft_depth}")
    perft.run_perft(pos, perft_depth, True)

    return

if __name__ == "__main__":
    main()