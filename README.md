# perft-by-lang
A benchmark for speed across different programming languages, via chess move generation (perft).<br>
Languages in list:
- C++

## Implementation details
Each program / script will use bitboards and mailbox for move generation, particularly magic bitboards for generating slider moves (bishops, rooks and queens).<br>
Core movegen is based on BBC (by Maksim Korzh) while board representation is based on VICE (by Richard Allbert). The codebase is a simplified version of the one used in [Dragonrose](https://github.com/TampliteSK/Dragonrose_Cpp/) chess engine.<br>

## Statistics
|    Language   | Perft Depth / NPS |
| ------------- | ----------------- |
|      C++      |  Depth 6 / 26.6M  |
|       C       |  Depth 5 / 69.4M  |