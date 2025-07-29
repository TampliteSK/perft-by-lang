# perft-by-lang
A benchmark for speed across different programming languages, via chess move generation (perft).<br>
Languages in list:
- C++

## Implementation details
Each program / script will use bitboards and mailbox for move generation, particularly magic bitboards for generating slider moves (bishops, rooks and queens). Core movegen is based on BBC (by Maksim Korzh) while board representation is based on VICE (by Richard Allbert).<br>
The C++ codebase is a simplified version of the one used in [Dragonrose](https://github.com/TampliteSK/Dragonrose_Cpp/) chess engine. The C codebase is a direct C translation of it (the C++ code is already written in a C-style anyway). Any declarative programming language shall be a loose translation of the same thing.

## Statistics
|    Language   | Perft Depth / NPS |
|:-------------:|:-----------------:|
|      C++      |  Depth 6 / 26.6M  |
|     Pony      | Depth 69 / 69.4M  |