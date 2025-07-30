# attackgen.py

from datatypes import Squares, Colour
from Bitboard import Bitboard
from attackmagics import bishop_magic_numbers, rook_magic_numbers, bishop_relevant_bits, rook_relevant_bits, not_a_file, not_h_file, not_hg_file, not_ab_file

# Attack tables and masks
pawn_attacks = [[Bitboard() for _ in range(64)] for _ in range(2)]  # [side][square]
knight_attacks = [Bitboard() for _ in range(64)]
king_attacks = [Bitboard() for _ in range(64)]
bishop_masks = [Bitboard() for _ in range(64)]
rook_masks = [Bitboard() for _ in range(64)]
bishop_attacks = [[Bitboard() for _ in range(512)] for _ in range(64)]
rook_attacks = [[Bitboard() for _ in range(4096)] for _ in range(64)]

"""
    Leapers attackgen
"""

# generate pawn attacks
def mask_pawn_attacks(side: Colour, sq: Squares) -> Bitboard:

    attacks = Bitboard()
    bitboard = Bitboard()
    bitboard.set_bit(sq)

    # White pawns
    if side == Colour.WHITE:
        if ((bitboard >> 7) & not_a_file): attacks |= (bitboard >> 7)
        if ((bitboard >> 9) & not_h_file): attacks |= (bitboard >> 9)
    # Black pawns
    else:
        if ((bitboard << 7) & not_h_file): attacks |= (bitboard << 7)
        if ((bitboard << 9) & not_a_file): attacks |= (bitboard << 9)

    return Bitboard(attacks)

# generate knight attacks
def mask_knight_attacks(sq: Squares) -> Bitboard:

    attacks = Bitboard()
    bitboard = Bitboard()
    bitboard.set_bit(sq)

    if ((bitboard >> 17) & not_h_file):  attacks |= (bitboard >> 17)
    if ((bitboard >> 15) & not_a_file):  attacks |= (bitboard >> 15)
    if ((bitboard >> 10) & not_hg_file): attacks |= (bitboard >> 10)
    if ((bitboard >> 6) & not_ab_file):  attacks |= (bitboard >> 6)
    if ((bitboard << 17) & not_a_file):  attacks |= (bitboard << 17)
    if ((bitboard << 15) & not_h_file):  attacks |= (bitboard << 15)
    if ((bitboard << 10) & not_ab_file): attacks |= (bitboard << 10)
    if ((bitboard << 6) & not_hg_file):  attacks |= (bitboard << 6)
    return Bitboard(attacks)

# generate king attacks
def mask_king_attacks(sq: Squares) -> Bitboard:
    attacks = Bitboard()
    bitboard = Bitboard()
    bitboard.set_bit(sq)

    if (bitboard >> 8): attacks |= (bitboard >> 8)
    if ((bitboard >> 9) & not_h_file): attacks |= (bitboard >> 9)
    if ((bitboard >> 7) & not_a_file): attacks |= (bitboard >> 7)
    if ((bitboard >> 1) & not_h_file): attacks |= (bitboard >> 1)
    if (bitboard << 8): attacks |= (bitboard << 8)
    if ((bitboard << 9) & not_a_file): attacks |= (bitboard << 9)
    if ((bitboard << 7) & not_h_file): attacks |= (bitboard << 7)
    if ((bitboard << 1) & not_a_file): attacks |= (bitboard << 1)
    return Bitboard(attacks)

"""
    Sliders attackgen
"""

# mask bishop attacks
def mask_bishop_attacks(sq: Squares) -> Bitboard:
    attacks = Bitboard()
    tr: int = sq.value // 8
    tf: int = sq.value % 8
    
    for r, f in zip(range(tr + 1, 7), range(tf + 1, 7)):
        attacks |= Bitboard(1 << (r * 8 + f))
    for r, f in zip(range(tr - 1, 0, -1), range(tf + 1, 7)):
        attacks |= Bitboard(1 << (r * 8 + f))
    for r, f in zip(range(tr + 1, 7), range(tf - 1, 0, -1)):
        attacks |= Bitboard(1 << (r * 8 + f))
    for r, f in zip(range(tr - 1, 0, -1), range(tf - 1, 0, -1)):
        attacks |= Bitboard(1 << (r * 8 + f))
    return Bitboard(attacks)

# mask rook attacks
def mask_rook_attacks(sq: Squares) -> Bitboard:
    attacks = Bitboard()
    tr: int = sq.value // 8
    tf: int = sq.value % 8

    for r in range(tr + 1, 7):
        attacks |= Bitboard(1 << (r * 8 + tf))
    for r in range(tr - 1, 0, -1):
        attacks |= Bitboard(1 << (r * 8 + tf))
    for f in range(tf + 1, 7):
        attacks |= Bitboard(1 << (tr * 8 + f))
    for f in range(tf - 1, 0, -1):
        attacks |= Bitboard(1 << (tr * 8 + f))
    return Bitboard(attacks)

# generate bishop attacks on the fly
def bishop_attacks_on_the_fly(sq: Squares, blockers: Bitboard) -> Bitboard:
    attacks = Bitboard()
    tr: int = sq.value // 8
    tf: int = sq.value % 8

    # up-right
    r, f = tr + 1, tf + 1
    while r <= 7 and f <= 7:
        attacks |= Bitboard(1 << (r * 8 + f))
        if Bitboard(1 << (r * 8 + f)) & blockers:
            break
        r += 1
        f += 1
    # down-right
    r, f = tr - 1, tf + 1
    while r >= 0 and f <= 7:
        attacks |= Bitboard(1 << (r * 8 + f))
        if Bitboard(1 << (r * 8 + f)) & blockers:
            break
        r -= 1
        f += 1
    # up-left
    r, f = tr + 1, tf - 1
    while r <= 7 and f >= 0:
        attacks |= Bitboard(1 << (r * 8 + f))
        if Bitboard(1 << (r * 8 + f)) & blockers:
            break
        r += 1
        f -= 1
    # down-left
    r, f = tr - 1, tf - 1
    while r >= 0 and f >= 0:
        attacks |= Bitboard(1 << (r * 8 + f))
        if Bitboard(1 << (r * 8 + f)) & blockers:
            break
        r -= 1
        f -= 1
    return Bitboard(attacks)

# generate rook attacks on the fly
def rook_attacks_on_the_fly(sq: Squares, blockers: Bitboard) -> Bitboard:
    attacks = Bitboard()
    tr: int = sq.value // 8
    tf: int = sq.value % 8
    # up
    for r in range(tr + 1, 8):
        attacks |= Bitboard(1 << (r * 8 + tf))
        if Bitboard(1 << (r * 8 + tf)) & blockers:
            break
    # down
    for r in range(tr - 1, -1, -1):
        attacks |= Bitboard(1 << (r * 8 + tf))
        if Bitboard(1 << (r * 8 + tf)) & blockers:
            break
    # right
    for f in range(tf + 1, 8):
        attacks |= Bitboard(1 << (tr * 8 + f))
        if Bitboard(1 << (tr * 8 + f)) & blockers:
            break
    # left
    for f in range(tf - 1, -1, -1):
        attacks |= Bitboard(1 << (tr * 8 + f))
        if Bitboard(1 << (tr * 8 + f)) & blockers:
            break
    return Bitboard(attacks)

# get bishop attacks
def get_bishop_attacks(sq: Squares, occupancy: Bitboard) -> Bitboard:
    occ = int(occupancy & bishop_masks[sq.value])
    occ *= bishop_magic_numbers[sq.value]
    occ >>= 64 - bishop_relevant_bits[sq.value] 
    if occ >= len(bishop_attacks[sq.value]):
        print(f"Debug: occ={occ}, sq={sq}, mask={int(bishop_masks[sq.value])}, occ_in={int(occupancy)}, magic={bishop_magic_numbers[sq.value]}, relbits={bishop_relevant_bits[sq.value]}")
        occupancy.print_bitboard()
        mask = Bitboard(bishop_masks[sq.value])
        mask.print_bitboard()
        raise ValueError(f"Invalid occ {occ} for bishop_attacks[{sq.value}]")
    return bishop_attacks[sq.value][occ]

# get rook attacks
def get_rook_attacks(sq: Squares, occupancy: Bitboard) -> Bitboard:
    occ = int(occupancy & rook_masks[sq.value])
    occ *= rook_magic_numbers[sq.value]
    occ >>= 64 - rook_relevant_bits[sq.value]
    return rook_attacks[sq.value][occ]

# get queen attacks
def get_queen_attacks(sq: Squares, occupancy: Bitboard) -> Bitboard:
    return Bitboard(get_bishop_attacks(sq, occupancy) | get_rook_attacks(sq, occupancy))

"""
    Master functions
"""

# init leaper pieces attacks
def init_leapers_attacks():
    for square in Squares:
        if square != Squares.NO_SQ:
            pawn_attacks[Colour.WHITE.value][square.value] = mask_pawn_attacks(Colour.WHITE, square)
            pawn_attacks[Colour.BLACK.value][square.value] = mask_pawn_attacks(Colour.BLACK, square)
            knight_attacks[square.value] = mask_knight_attacks(square)
            king_attacks[square.value] = mask_king_attacks(square)

# set occupancies
def set_occupancy(index: int, bits_in_mask: int, attack_mask: Bitboard) -> Bitboard:
    copy = attack_mask
    occupancy = Bitboard()
    for count in range(bits_in_mask):
        square, copy = copy.pop_ls1b()
        if square == -1:
            break
        if index & (1 << count):
            occupancy.set_bit(square)
    return Bitboard(occupancy)


# init slider piece's attack tables
def init_sliders_attacks(bishop: bool):
    for square in Squares:
        if square != Squares.NO_SQ:
            bishop_masks[square.value] = mask_bishop_attacks(square)
            rook_masks[square.value] = mask_rook_attacks(square)
            attack_mask = bishop_masks[square.value] if bishop else rook_masks[square.value]
            relevant_bits_count = attack_mask.count_bits()
            occupancy_indices = 1 << relevant_bits_count
            for index in range(occupancy_indices):
                occupancy = set_occupancy(index, relevant_bits_count, attack_mask)
                if bishop:
                    magic_index = (occupancy * bishop_magic_numbers[square.value]) >> (64 - bishop_relevant_bits[square.value])
                    bishop_attacks[square.value][magic_index] = bishop_attacks_on_the_fly(square, occupancy)
                else:
                    magic_index = (occupancy * rook_magic_numbers[square.value]) >> (64 - rook_relevant_bits[square.value])
                    rook_attacks[square.value][magic_index] = rook_attacks_on_the_fly(square, occupancy)


def init_attack_tables():
    init_leapers_attacks()
    init_sliders_attacks(True)   # Bishop
    init_sliders_attacks(False)  # Rook