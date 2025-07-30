# bitboard.py: A class wrapper over int with common bitboard operations

from datatypes import Squares

class Bitboard(int):
    """
    A class representing a bitboard, which is a 64-bit integer used to represent
    the state of a chessboard.
    """
    
    # Creates an instance, no __init__ required
    def __new__(cls, value=0):
        return super().__new__(cls, value)

    def __str__(self):
        return f"Bitboard({self:#018x})"

    # Common bitboard operations
    def get_bit(self, square: Squares) -> int:
        """
        Returns the bit at the specified square.
        """
        return (self >> square.value) & 1
    
    def set_bit(self, square: Squares) -> 'Bitboard':
        """
        Sets the bit at the specified square.
        """
        return Bitboard(self | (1 << square.value))
    
    def clear_bit(self, square: Squares) -> 'Bitboard':
        """
        Clears the bit at the specified square.
        """
        return Bitboard(self & ~(1 << square.value))
    
    def pop_ls1b(self) -> tuple[Squares, 'Bitboard']:
        """
        Clears the least significant set bit and returns its index (0-63) and the new bitboard.
        """
        if self == 0:
            print("Warning: Attempted to pop from an empty bitboard.")
            return Squares.NO_SQ, self
        
        index = (self & -self).bit_length() - 1
        new_bb = self & (self - 1)
        return Squares(index), Bitboard(new_bb)
        
    def count_bits(self) -> int:
        """
        Counts the number of bits set in the bitboard.
        """
        return bin(self).count('1')
    
    # Bitwise operations
    def __and__(self, other: 'Bitboard') -> 'Bitboard':
        return Bitboard(super().__and__(other))

    def __or__(self, other: 'Bitboard') -> 'Bitboard':
        return Bitboard(super().__or__(other))

    def __xor__(self, other: 'Bitboard') -> 'Bitboard':
        return Bitboard(super().__xor__(other))

    def __invert__(self) -> 'Bitboard':
        return Bitboard(super().__invert__())

    # In-place bitwise operations
    def __iand__(self, other: 'Bitboard') -> 'Bitboard':
        return self.__and__(other)

    def __ior__(self, other: 'Bitboard') -> 'Bitboard':
        return self.__or__(other)

    def __ixor__(self, other: 'Bitboard') -> 'Bitboard':
        return self.__xor__(other)

    # Output
    def print_bitboard(self):
        """
        Prints the bitboard in a human-readable format.
        """
        print("\n")
        for rank in range(7, -1, -1):
            print(f"{rank + 1}   ", end="")
            for file in range(8):
                sq = rank * 8 + file
                if self.get_bit(Squares(sq)):
                    print("X", end="")
                else:
                    print("-", end="")
            print()
        print("  ABCDEFGH\n")
        print(f"Bits set: {self.count_bits()}\n")