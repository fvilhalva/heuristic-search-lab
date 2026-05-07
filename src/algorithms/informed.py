"""Implementation of informed search algorithms."""

import heapq
from typing import Optional, List
from src.utils.node import Node


class SearchResult:
    """Result of a search."""

    def __init__(
        self,
        node: Optional[Node],
        problem,
        expanded_nodes: int = 0,
        frontier_max_size: int = 0,
    ):
        self.node = node
        self.problem = problem
        self.expanded_nodes = expanded_nodes
        self.frontier_max_size = frontier_max_size

    @property
    def path(self) -> List:
        """Return the path from start to goal."""
        if self.node is None:
            return []
        return self.node.path()

    @property
    def depth(self) -> int:
        """Return the depth of the solution."""
        return self.node.depth if self.node else 0

    @property
    def cost(self) -> float:
        """Return the cost of the solution."""
        return self.node.path_cost if self.node else 0


class GreedySearch:
    """Greedy Search - expands node with lowest heuristic value."""

    def solve(self, problem) -> SearchResult:
        """Find solution using Greedy Search."""
        start = Node(
            state=problem.initial_state,
            depth=0,
            path_cost=0,
            priority=problem.heuristic(problem.initial_state),
        )

        if problem.goal_test(start.state):
            return SearchResult(start, problem, expanded_nodes=0)

        frontier = [(start.priority, id(start), start)]
        explored = set()
        expanded_nodes = 0
        max_frontier_size = 1
        counter = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            h_value, _, node = heapq.heappop(frontier)

            if problem.goal_test(node.state):
                return SearchResult(node, problem, expanded_nodes, max_frontier_size)

            if node.state in explored:
                continue

            explored.add(node.state)
            expanded_nodes += 1

            for action in problem.actions(node.state):
                child_state = problem.result(node.state, action)

                if child_state not in explored:
                    h_value = problem.heuristic(child_state)
                    child = Node(
                        state=child_state,
                        parent=node,
                        action=action,
                        depth=node.depth + 1,
                        path_cost=node.path_cost + 1,
                        priority=h_value,
                    )
                    heapq.heappush(frontier, (h_value, counter, child))
                    counter += 1

        return SearchResult(None, problem, expanded_nodes, max_frontier_size)


class AStarSearch:
    """A* Search - expands node with lowest f(n) = g(n) + h(n)."""

    def solve(self, problem) -> SearchResult:
        """Find solution using A* Search."""
        h_value = problem.heuristic(problem.initial_state)
        start = Node(
            state=problem.initial_state,
            depth=0,
            path_cost=0,
            priority=h_value,  # f(n) = 0 + h(n)
        )

        if problem.goal_test(start.state):
            return SearchResult(start, problem, expanded_nodes=0)

        frontier = [(start.priority, id(start), start)]
        explored = set()
        expanded_nodes = 0
        max_frontier_size = 1
        counter = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            f_value, _, node = heapq.heappop(frontier)

            if problem.goal_test(node.state):
                return SearchResult(node, problem, expanded_nodes, max_frontier_size)

            if node.state in explored:
                continue

            explored.add(node.state)
            expanded_nodes += 1

            for action in problem.actions(node.state):
                child_state = problem.result(node.state, action)

                if child_state not in explored:
                    # For Romania map and similar graphs, get distance
                    if hasattr(problem, "get_distance"):
                        step_cost = problem.get_distance(node.state, child_state)
                    else:
                        step_cost = 1

                    g_value = node.path_cost + step_cost
                    h_value = problem.heuristic(child_state)
                    f_value = g_value + h_value

                    child = Node(
                        state=child_state,
                        parent=node,
                        action=action,
                        depth=node.depth + 1,
                        path_cost=g_value,
                        priority=f_value,
                    )
                    heapq.heappush(frontier, (f_value, counter, child))
                    counter += 1

        return SearchResult(None, problem, expanded_nodes, max_frontier_size)
