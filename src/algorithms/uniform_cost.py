"""Implementation of uniform-cost search."""

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


class UniformCostSearch:
    """Uniform-Cost Search - expands least cost nodes first."""

    def solve(self, problem) -> SearchResult:
        """Find solution using Uniform-Cost Search."""
        start = Node(state=problem.initial_state, depth=0, path_cost=0, priority=0)

        if problem.goal_test(start.state):
            return SearchResult(start, problem, expanded_nodes=0)

        frontier = [(0, id(start), start)]  # (cost, unique_id, node)
        explored = set()
        expanded_nodes = 0
        max_frontier_size = 1
        counter = 1  # For unique IDs

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            cost, _, node = heapq.heappop(frontier)

            if problem.goal_test(node.state):
                return SearchResult(node, problem, expanded_nodes, max_frontier_size)

            if node.state in explored:
                continue

            explored.add(node.state)
            expanded_nodes += 1

            for action in problem.actions(node.state):
                child_state = problem.result(node.state, action)

                # For Romania map and similar graphs, get distance
                if hasattr(problem, "get_distance"):
                    step_cost = problem.get_distance(node.state, child_state)
                else:
                    step_cost = 1

                child_cost = node.path_cost + step_cost

                if child_state not in explored:
                    child = Node(
                        state=child_state,
                        parent=node,
                        action=action,
                        depth=node.depth + 1,
                        path_cost=child_cost,
                        priority=child_cost,
                    )
                    heapq.heappush(frontier, (child_cost, counter, child))
                    counter += 1

        return SearchResult(None, problem, expanded_nodes, max_frontier_size)
