"""Interactive entry point for the heuristic search lab.

The teacher can type the problem input, choose the algorithm, and inspect the
solution path, cost, expansion order, and execution metrics.
"""

from __future__ import annotations

from typing import Iterable, Tuple

from src.algorithms.informed import AStarSearch, GreedySearch
from src.algorithms.uniform_cost import UniformCostSearch
from src.algorithms.uninformed import BFS, DFS
from src.graphs.romania_map import RomaniaMap
from src.puzzles.eight_puzzle import EightPuzzle
from src.utils.search_result import SearchResult


ALGORITHMS = {
    "1": ("BFS / Busca em Largura", BFS),
    "2": ("DFS / Busca em Profundidade", DFS),
    "3": ("Busca de Custo Uniforme", UniformCostSearch),
    "4": ("Greedy / Busca Gulosa", GreedySearch),
    "5": ("A*", AStarSearch),
}


def line() -> None:
    print("-" * 72)


def title(text: str) -> None:
    print("\n" + "=" * 72)
    print(text)
    print("=" * 72)


def format_puzzle_state(state: Tuple[int, ...]) -> str:
    """Format an 8-puzzle state as a 3x3 board."""
    cells = ["_" if value == 0 else str(value) for value in state]
    rows = [" ".join(cells[i : i + 3]) for i in range(0, 9, 3)]
    return "\n".join(rows)


def format_state(state) -> str:
    if isinstance(state, tuple) and len(state) == 9:
        return "\n" + format_puzzle_state(state)
    return str(state)


def print_result(result: SearchResult, algorithm_name: str) -> None:
    """Pretty-print search results."""
    title(f"Resultado - {algorithm_name}")

    if result.node is None:
        print("Solução não encontrada.")
        print(f"Nós expandidos: {result.expanded_nodes}")
        print(f"Tamanho máximo da fronteira: {result.frontier_max_size}")
        print(f"Tempo de execução: {result.elapsed_time:.6f} s")
        return

    print("Solução encontrada.")
    print(f"Profundidade / número de passos: {result.depth}")
    print(f"Custo total: {result.cost:g}")
    print(f"Nós expandidos: {result.expanded_nodes}")
    print(f"Tamanho máximo da fronteira: {result.frontier_max_size}")
    print(f"Tempo de execução: {result.elapsed_time:.6f} s")

    if result.expansion_order:
        line()
        print("Ordem de expansão:")
        for index, state in enumerate(result.expansion_order, start=1):
            print(f"{index}. {format_state(state)}")

    line()
    print("Caminho solução:")
    for index, node in enumerate(result.path):
        action = "início" if node.action is None else f"ação: {node.action}"
        print(f"\nPasso {index} ({action}, g={node.path_cost:g}):")
        print(format_state(node.state))


def choose_algorithm():
    """Ask the user to choose a search algorithm."""
    print("\nAlgoritmos disponíveis:")
    for key, (name, _) in ALGORITHMS.items():
        print(f"{key} - {name}")

    while True:
        choice = input("Escolha o algoritmo: ").strip()
        if choice in ALGORITHMS:
            name, algorithm_class = ALGORITHMS[choice]
            if choice == "2":
                limit = input("Limite de profundidade para DFS [50]: ").strip()
                depth_limit = int(limit) if limit else 50
                return name, algorithm_class(depth_limit=depth_limit)
            return name, algorithm_class()
        print("Opção inválida.")


def read_city(prompt: str, default: str | None = None) -> str:
    """Read and validate a Romania map city."""
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        city = RomaniaMap.normalize_city(raw)
        if city in RomaniaMap.GRAPH:
            return city
        print("Cidade inválida. Cidades disponíveis:")
        print(", ".join(RomaniaMap.cities()))


def run_romania() -> None:
    """Run one algorithm on the Romania map problem using typed input."""
    title("Mapa da Romênia")
    print("Cidades disponíveis:")
    print(", ".join(RomaniaMap.cities()))

    initial_city = read_city("Cidade inicial [Arad]: ", default="Arad")
    goal_city = read_city("Cidade objetivo [Bucharest]: ", default="Bucharest")

    problem = RomaniaMap(initial_city, goal_city)
    if goal_city != "Bucharest":
        print("\nObservação: a heurística em linha reta disponível é para Bucharest.")
        print("Para outro objetivo, h(n)=0; A* fica equivalente à busca de custo uniforme.")

    algorithm_name, algorithm = choose_algorithm()
    result = algorithm.solve(problem)
    print_result(result, algorithm_name)


def parse_puzzle_state(text: str) -> Tuple[int, ...]:
    """Parse a typed 8-puzzle state.

    Accepted formats:
      1 2 3 4 0 5 6 7 8
      123405678
      1,2,3,4,0,5,6,7,8
    """
    cleaned = text.replace(",", " ").replace(";", " ").replace("_", "0")
    parts = cleaned.split()

    if len(parts) == 1 and len(parts[0]) == 9 and parts[0].isdigit():
        values = [int(char) for char in parts[0]]
    else:
        values = [int(part) for part in parts]

    state = tuple(values)
    EightPuzzle.validate_state(state)
    return state


def read_puzzle_state(prompt: str, default: Tuple[int, ...] | None = None) -> Tuple[int, ...]:
    """Read and validate an 8-puzzle state from input."""
    while True:
        text = input(prompt).strip()
        if not text and default is not None:
            return default
        try:
            return parse_puzzle_state(text)
        except ValueError as exc:
            print(f"Entrada inválida: {exc}")
            print("Digite 9 números de 0 a 8 sem repetição. Exemplo: 1 2 3 4 0 5 6 7 8")


def choose_heuristic() -> str:
    """Ask the user to choose the 8-puzzle heuristic."""
    print("\nHeurísticas para o 8-puzzle:")
    print("1 - Peças fora do lugar")
    print("2 - Distância Manhattan")
    print("3 - Zero / sem heurística")
    while True:
        choice = input("Escolha a heurística [2]: ").strip() or "2"
        if choice == "1":
            return "misplaced"
        if choice == "2":
            return "manhattan"
        if choice == "3":
            return "zero"
        print("Opção inválida.")


def run_puzzle() -> None:
    """Run one algorithm on the 8-puzzle using typed input."""
    title("8-Puzzle")
    print("Use 0 ou _ para representar o espaço vazio.")
    print("Exemplo do quadro: 1 2 3 4 0 5 6 7 8")

    default_goal = (1, 2, 3, 4, 0, 5, 6, 7, 8)
    initial_state = read_puzzle_state("Estado inicial: ")
    goal_state = read_puzzle_state(
        "Estado objetivo [1 2 3 4 0 5 6 7 8]: ",
        default=default_goal,
    )

    heuristic_name = choose_heuristic()
    problem = EightPuzzle(initial_state, goal_state, heuristic_name=heuristic_name)

    if not problem.is_solvable():
        print("\nEste estado inicial não alcança o objetivo informado.")
        print("O programa não executará a busca para evitar uma exploração desnecessária.")
        return

    algorithm_name, algorithm = choose_algorithm()
    result = algorithm.solve(problem)
    print_result(result, algorithm_name)


def run_quick_demo() -> None:
    """Run a small automatic demo useful for quick testing."""
    title("Demonstração rápida")
    problem = RomaniaMap("Arad", "Bucharest")
    for algorithm_name, algorithm in [
        ("BFS / Busca em Largura", BFS()),
        ("DFS / Busca em Profundidade", DFS(depth_limit=20)),
        ("Busca de Custo Uniforme", UniformCostSearch()),
        ("Greedy / Busca Gulosa", GreedySearch()),
        ("A*", AStarSearch()),
    ]:
        result = algorithm.solve(problem)
        print_result(result, algorithm_name)


def main() -> None:
    """Interactive menu."""
    while True:
        title("Heuristic Search Lab")
        print("1 - Resolver Mapa da Romênia")
        print("2 - Resolver 8-Puzzle")
        print("3 - Rodar demonstração rápida")
        print("0 - Sair")

        choice = input("Escolha uma opção: ").strip()
        if choice == "1":
            run_romania()
        elif choice == "2":
            run_puzzle()
        elif choice == "3":
            run_quick_demo()
        elif choice == "0":
            print("Encerrando.")
            break
        else:
            print("Opção inválida.")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
