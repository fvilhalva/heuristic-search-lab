"""Implementation of uniform-cost search."""

from __future__ import annotations

import heapq
import time
from typing import Any

from src.utils.node import Node
from src.utils.search_result import SearchResult


def _step_cost(problem: Any, state: Any, next_state: Any) -> float:
    if hasattr(problem, "get_distance"):
        return problem.get_distance(state, next_state)
    if hasattr(problem, "step_cost"):
        return problem.step_cost(state, next_state)
    return 1.0


class UniformCostSearch:
    """Uniform-Cost Search - expands the node with the lowest path cost g(n)."""

    def solve(self, problem) -> SearchResult:
        """Find a solution using Uniform-Cost Search."""
        start_time = time.perf_counter()
        start = Node(state=problem.initial_state, depth=0, path_cost=0.0, priority=0.0)

        frontier = [(0.0, 0, start)]
        best_cost = {start.state: 0.0}
        explored = set()
        expansion_order = []
        expanded_nodes = 0
        max_frontier_size = 1
        counter = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            cost, _, node = heapq.heappop(frontier)

            if cost > best_cost.get(node.state, float("inf")):
                continue

            if problem.goal_test(node.state):
                return SearchResult(
                    node,
                    problem,
                    expanded_nodes,
                    max_frontier_size,
                    expansion_order,
                    time.perf_counter() - start_time,
                )

            if node.state in explored:
                continue

            explored.add(node.state)
            expansion_order.append(node.state)
            expanded_nodes += 1

            for action in problem.actions(node.state):
                child_state = problem.result(node.state, action)
                child_cost = node.path_cost + _step_cost(problem, node.state, child_state)

                if child_cost >= best_cost.get(child_state, float("inf")):
                    continue

                best_cost[child_state] = child_cost
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

        return SearchResult(
            None,
            problem,
            expanded_nodes,
            max_frontier_size,
            expansion_order,
            time.perf_counter() - start_time,
        )
