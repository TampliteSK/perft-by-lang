# Compiler selection
CXX ?= g++
SRCS = $(wildcard src/*.cpp)
EXE ?= perft_cpp

# Compiler flags
STD_FLAGS = -std=c++20
WARN_FLAGS = -Wall -Werror -Wextra -Wno-error=vla -Wpedantic
OPT_FLAGS = -O3 -ffast-math -march=native -funroll-loops
CXXFLAGS = $(STD_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS)

# Add .exe if Windows
ifeq ($(OS),Windows_NT)
    EXE := $(EXE).exe
endif

# Build target
all:
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(EXE)

clean:
	rm -f $(EXE)