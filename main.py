"""Entry point for the heuristic search lab.

Demonstrates different search algorithms solving classic AI problems.
"""

from src.algorithms.uninformed import BFS, DFS
from src.algorithms.uniform_cost import UniformCostSearch
from src.algorithms.informed import GreedySearch, AStarSearch
from src.puzzles.eight_puzzle import EightPuzzle
from src.graphs.romania_map import RomaniaMap


def print_result(result, algorithm_name: str):
    """Pretty print search results."""
    print(f"\n{'='*60}")
    print(f"Algorithm: {algorithm_name}")
    print(f"{'='*60}")

    if result.node:
        print(f"✓ Solution found!")
        print(f"  Depth: {result.depth}")
        print(f"  Cost: {result.cost}")
        print(f"  Nodes expanded: {result.expanded_nodes}")
        print(f"  Max frontier size: {result.frontier_max_size}")

        path = result.path
        print(f"\n  Path ({len(path)} steps):")
        for i, node in enumerate(path):
            if i == 0:
                print(f"    {i}: {node.state} (start)")
            else:
                print(f"    {i}: {node.state} (action: {node.action})")
    else:
        print(f"✗ No solution found!")
        print(f"  Nodes expanded: {result.expanded_nodes}")
        print(f"  Max frontier size: {result.frontier_max_size}")


def demo_8puzzle():
    """Demonstrate search algorithms on the 8-puzzle problem."""
    print("\n" + "🧩 " * 20)
    print("8-PUZZLE PROBLEM")
    print("🧩 " * 20)

    # Initial state: scrambled puzzle
    # Goal state: numbers 1-8 in order with 0 (empty space) at position 0
    initial_state = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    puzzle = EightPuzzle(initial_state, goal_state)

    # Try different algorithms
    algorithms = [
        ("BFS (Breadth-First Search)", BFS()),
        ("DFS (Depth-First Search)", DFS()),
        ("A* Search", AStarSearch()),
    ]

    for algo_name, algo in algorithms:
        result = algo.solve(puzzle)
        print_result(result, algo_name)


def demo_romania_map():
    """Demonstrate search algorithms on the Romania map problem."""
    print("\n" + "🗺️  " * 20)
    print("ROMANIA MAP PROBLEM - Arad to Bucharest")
    print("🗺️  " * 20)

    initial_city = "Arad"
    goal_city = "Bucharest"

    map_problem = RomaniaMap(initial_city, goal_city)

    # Try different algorithms
    algorithms = [
        ("BFS (Breadth-First Search)", BFS()),
        ("DFS (Depth-First Search)", DFS()),
        ("Uniform-Cost Search", UniformCostSearch()),
        ("Greedy Search", GreedySearch()),
        ("A* Search", AStarSearch()),
    ]

    for algo_name, algo in algorithms:
        result = algo.solve(map_problem)
        print_result(result, algo_name)


def demo_simple_puzzle():
    """Demonstrate with a simpler puzzle that can be solved quickly."""
    print("\n" + "🧩 " * 20)
    print("SIMPLE 8-PUZZLE (easier to solve)")
    print("🧩 " * 20)

    # This is very close to goal, should be solvable by all algorithms
    initial_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    puzzle = EightPuzzle(initial_state, goal_state)

    algorithms = [
        ("BFS (Breadth-First Search)", BFS()),
        ("A* Search", AStarSearch()),
    ]

    for algo_name, algo in algorithms:
        result = algo.solve(puzzle)
        print_result(result, algo_name)


def main() -> None:
    """Run all demonstrations."""
    print("\n" + "=" * 60)
    print("HEURISTIC SEARCH LAB")
    print("Algorithms on Classic AI Problems")
    print("=" * 60)

    # Run demonstrations
    demo_simple_puzzle()
    demo_romania_map()
    # Uncomment to run 8-puzzle demo (may take longer)
    # demo_8puzzle()

    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
