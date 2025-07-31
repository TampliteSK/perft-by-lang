# main.py

from attackgen import init_attack_tables
import Board
import perft
import cProfile
from bitboard import *
from datatypes import *
from Move import Move
from makemove import make_move

def main(argc: int, argv: list):
    
    # profiler = cProfile.Profile()
    # profiler.enable()
    start = perft.get_time_ms()
    init_attack_tables()
    print(f"Attack tables initialised in {perft.get_time_ms() - start}ms")
    # profiler.disable()
    # profiler.print_stats(sort='cumtime')  # Sort by cumulative time

    pos = Board.Board()
    pos.reset_board()
    pos.parse_fen(Board.START_POS)
    #pos.print_board()
    #move = Move.encode(Squares.a2, Squares.a3, Piece.wP, Piece.EMPTY, Piece.EMPTY, 1, 0, 0)
    #make_move(pos, move)
    #pos.print_board()

    perft_depth = 3
    if argc > 1:
        input = int(argv[1])
        if input < 1 or input > 10:
            print("Invalid depth. Please enter a value between 1 and 10.")
            return
        perft_depth = int(argv[1])

    # Run performance test
    print(f"Running perft with depth: {perft_depth}")
    perft.run_perft(pos, perft_depth, True)

    return

if __name__ == "__main__":
    main(0, [])