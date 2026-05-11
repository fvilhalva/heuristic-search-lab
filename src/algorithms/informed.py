"""Implementation of informed search algorithms."""

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


class GreedySearch:
    """Greedy Best-First Search - expands the node with the lowest h(n)."""

    def solve(self, problem) -> SearchResult:
        """Find a solution using Greedy Search."""
        start_time = time.perf_counter()
        start_h = problem.heuristic(problem.initial_state)
        start = Node(state=problem.initial_state, depth=0, path_cost=0.0, priority=start_h)

        frontier = [(start_h, 0, start)]
        frontier_states = {start.state}
        explored = set()
        expansion_order = []
        expanded_nodes = 0
        max_frontier_size = 1
        counter = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, _, node = heapq.heappop(frontier)
            frontier_states.discard(node.state)

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
                if child_state in explored or child_state in frontier_states:
                    continue

                h_value = problem.heuristic(child_state)
                child = Node(
                    state=child_state,
                    parent=node,
                    action=action,
                    depth=node.depth + 1,
                    path_cost=node.path_cost + _step_cost(problem, node.state, child_state),
                    priority=h_value,
                )
                heapq.heappush(frontier, (h_value, counter, child))
                frontier_states.add(child_state)
                counter += 1

        return SearchResult(
            None,
            problem,
            expanded_nodes,
            max_frontier_size,
            expansion_order,
            time.perf_counter() - start_time,
        )


class AStarSearch:
    """A* Search - expands the node with the lowest f(n) = g(n) + h(n)."""

    def solve(self, problem) -> SearchResult:
        """Find a solution using A* Search."""
        start_time = time.perf_counter()
        start_h = problem.heuristic(problem.initial_state)
        start = Node(state=problem.initial_state, depth=0, path_cost=0.0, priority=start_h)

        frontier = [(start_h, 0, start)]
        best_cost = {start.state: 0.0}
        explored = set()
        expansion_order = []
        expanded_nodes = 0
        max_frontier_size = 1
        counter = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, _, node = heapq.heappop(frontier)

            if node.path_cost > best_cost.get(node.state, float("inf")):
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
                g_value = node.path_cost + _step_cost(problem, node.state, child_state)

                if g_value >= best_cost.get(child_state, float("inf")):
                    continue

                best_cost[child_state] = g_value
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

        return SearchResult(
            None,
            problem,
            expanded_nodes,
            max_frontier_size,
            expansion_order,
            time.perf_counter() - start_time,
        )
