# Heuristic Search Lab

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-unittest-brightgreen)](#)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Python implementation of uninformed and informed search algorithms applied to the **8-puzzle**.

This repository provides an educational, interactive implementation of the 8-puzzle to demonstrate and compare search algorithms: BFS, DFS, Uniform Cost Search, Greedy and A* (with Manhattan heuristic), and an IDA* variant.

Features

- Simple, didactic implementations of common search algorithms.
- Input validation (size, tile uniqueness, solvability via inversion parity).
- Detailed output: solution path, cost, depth, expanded nodes, g(n), h(n), and f(n) when applicable.
- Terminal-based interactive interface for manual testing.

Implemented algorithms

- BFS (Breadth-First Search)
- DFS (Depth-First Search) with configurable depth limit
- Uniform Cost Search
- Greedy Best-First Search (with Manhattan heuristic)
- A* (with Manhattan heuristic)
- IDA* (Iterative Deepening A*)

About the 8-puzzle

The blank tile is represented by `0`. States are tuples of 9 integers containing the numbers 0..8 exactly once.

Example state:

```text
1 2 3
4 0 5
6 7 8
```

Validations performed by the program:

- Exactly 9 positions.
- The tiles 0..8 appear exactly once.
- The initial state is solvable to the goal state (inversion parity check).

Heuristic available:

- Manhattan distance (used by Greedy, A* and IDA*).

Usage

1. Clone or download the repository.
2. Run in the project directory:

```bash
python main.py
```

The program is interactive and will prompt for `initial state` and `goal state` as 9 space-separated numbers using `0` for the blank.

Example interactive input:

```text
initial state: 1 2 3 4 5 0 6 7 8
goal state:    1 2 3 4 0 5 6 7 8
Choose algorithm: 4
Use Manhattan heuristic? [y/n]: y
```

Metrics and output

When the search finishes the program prints:

- Solution path (states step by step).
- Total solution cost (`g(n)` of final node).
- Depth / number of moves.
- Number of expanded nodes during the search.
- `g(n)` values per state in the solution path.
- `h(n)` values when heuristics are used (Greedy, A*, IDA*).
- `f(n) = g(n) + h(n)` values for A*.

These metrics are useful to compare algorithms in terms of search effort and solution quality.

Project structure

```text
heuristic-search-lab/
├── LICENSE
├── main.py        # Main implementation and interactive interface
├── README.md      # Portuguese README
├── README_en.md   # English README (this file)
└── tests/         # Unit tests for functions and algorithms
    └── test_main.py
```

Tests

Run the unit tests with:

```bash
python -m unittest discover -s tests -v
```

Quick benchmark example

Use `time` or `python -m timeit` to measure simple cases. Example with `time`:

```bash
time python - <<'PY'
from time import perf_counter
import main

start = perf_counter()
main.busca_largura((1,2,3,4,5,6,7,0,8),(1,2,3,4,5,6,7,8,0))
end = perf_counter()
print('BFS time:', end - start)
PY
```

Contributing

Contributions are welcome. To contribute:

1. Open an issue describing your suggestion or bug
2. Fork the repository and create a branch for your change.
3. Send a pull request describing the changes and including tests when appropriate.

Ideas for improvements:

- Add alternative heuristics (e.g. misplaced tiles).
- Add richer step-by-step visualization (graphical or web UI).
- Performance optimizations and profiling.

License

This project is available under the license in the `LICENSE` file.

Author

Felipe Echeverria Vilhalva
