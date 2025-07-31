# perft.py

from time import time
from Board import Board
from Move import MoveList, Move
from movegen import generate_moves
from makemove import make_move, take_move

# Common test positions
"""
	Startpos - Depth 7 passed
	Kiwipete - Depth 5 passed
	CPW_Pos3 - Depth 7 passed
	CPW_Pos4 - Depth 6 passed
	CPW_Pos5 - Depth 6 passed (with webperft)
	CPW_Pos6 - Depth 6 passed

	Big thanks to Analog Hors for her webperft tool
"""
KIWIPETE = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -"
CPW_POS3 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
CPW_POS4 = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
CPW_POS5 = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
CPW_POS6 = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"

# Get time in milliseconds
def get_time_ms() -> int:
    return int(time() * 1000)

# Return total number of nodes
def run_perft(pos: Board, depth: int, print_info: bool) -> int:
    if depth == 0:
        return 0

    nodes = 0
    start = get_time_ms()

    move_list = MoveList()
    move_list = generate_moves(pos, move_list, False)
    # move_list.print_list()

    if print_info:
        print("\n     Performance test\n")
        start = get_time_ms()

    for move in move_list.moves:
        move_is_legal, pos = make_move(pos, move)
        if not move_is_legal:
            print(f"Illegal move: {move.print_move()}")
            continue

        old_nodes = nodes

        if depth == 1:
            nodes += 1
        else:
            nodes += run_perft(pos, depth - 1, False)

        new_nodes = nodes - old_nodes

        take_move(pos)

        # Print move if root level
        if (print_info):
            print(f"{move.print_move()}: {new_nodes}")

    # Print results if root level
    if print_info:
        time = get_time_ms() - start
        print(f"\n    Depth: {depth}")
        print(f"    Nodes: {nodes}")
        print(f"     Time: {time}ms ({time / 1000:.3f}s)")
        print(f"      NPS: {int(nodes / time * 1000)}\n")

    return nodes