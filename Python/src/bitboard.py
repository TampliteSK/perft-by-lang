# bitboard.py: Bitboard operation functions. No class as overhead is too high

from datatypes import Squares, Mirror64

type Bitboard = int

# Common bitboard operations
def get_bit(bitboard: int, square: Squares) -> int:
    """
    Returns the bit at the specified square.
    """
    return (bitboard >> square.value) & 1
    
def set_bit(bitboard: int, square: Squares) -> int:
    """
    Sets the bit at the specified square.
    """
    return bitboard | (1 << square.value)
    
def clear_bit(bitboard: int, square: Squares) -> int:
    """
    Clears the bit at the specified square.
    """
    return bitboard & ~(1 << square.value)

def pop_ls1b(bitboard: int) -> tuple[Squares, int]:
    """
    Clears the least significant set bit and returns its square index
    """
    bitboard &= 0xFFFFFFFFFFFFFFFF  # Ensure unsigned 64-bit
    if bitboard == 0:
        print("Warning: Attempted to pop from an empty bitboard.")
        return Squares.NO_SQ, bitboard
    
    index = (bitboard & -bitboard).bit_length() - 1
    bb = bitboard & (bitboard - 1)
    return Squares(index), bb
        
def count_bits(bitboard: int) -> int:
    """
    Counts the number of bits set in the bitboard.
    """
    return (bitboard & 0xFFFFFFFFFFFFFFFF).bit_count()

def print_bitboard(bitboard: int) -> None:
    """
    Prints the bitboard in a human-readable format.
    """
    print("\n")
    for rank in range(8):
        print(f"{8 - rank}   ", end="")
        for file in range(8):
            sq = rank * 8 + file
            if get_bit(bitboard, Squares(sq)):
                print("X", end="")
            else:
                print("-", end="")
        print()
    print("    ABCDEFGH\n")
    print(f"Bits set: {count_bits(bitboard)}")
    print(f"Value: {bitboard}\n")
    return