"""Implementation of uninformed search algorithms."""

from __future__ import annotations

import time
from collections import deque
from typing import Any

from src.utils.node import Node
from src.utils.search_result import SearchResult


def _step_cost(problem: Any, state: Any, next_state: Any) -> float:
    """Return the transition cost for a problem.

    Graph problems may define get_distance(). Puzzle moves usually cost 1.
    """
    if hasattr(problem, "get_distance"):
        return problem.get_distance(state, next_state)
    if hasattr(problem, "step_cost"):
        return problem.step_cost(state, next_state)
    return 1.0


class BFS:
    """Breadth-First Search - expands nodes level by level."""

    def solve(self, problem) -> SearchResult:
        """Find a solution using BFS."""
        start_time = time.perf_counter()
        start = Node(state=problem.initial_state, depth=0, path_cost=0.0)

        if problem.goal_test(start.state):
            return SearchResult(start, problem, expanded_nodes=0, elapsed_time=time.perf_counter() - start_time)

        frontier = deque([start])
        frontier_states = {start.state}
        explored = set()
        expansion_order = []
        expanded_nodes = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.popleft()
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

                child = Node(
                    state=child_state,
                    parent=node,
                    action=action,
                    depth=node.depth + 1,
                    path_cost=node.path_cost + _step_cost(problem, node.state, child_state),
                )
                frontier.append(child)
                frontier_states.add(child_state)

        return SearchResult(
            None,
            problem,
            expanded_nodes,
            max_frontier_size,
            expansion_order,
            time.perf_counter() - start_time,
        )


class DFS:
    """Depth-First Search - expands nodes in depth-first order."""

    def __init__(self, depth_limit: int | None = 50):
        self.depth_limit = depth_limit

    def solve(self, problem) -> SearchResult:
        """Find a solution using DFS.

        A default depth limit is used to avoid very deep/infinite paths in cyclic spaces.
        """
        start_time = time.perf_counter()
        start = Node(state=problem.initial_state, depth=0, path_cost=0.0)

        if problem.goal_test(start.state):
            return SearchResult(start, problem, expanded_nodes=0, elapsed_time=time.perf_counter() - start_time)

        frontier = [start]
        frontier_states = {start.state}
        explored = set()
        expansion_order = []
        expanded_nodes = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.pop()
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

            if self.depth_limit is not None and node.depth >= self.depth_limit:
                continue

            for action in reversed(problem.actions(node.state)):
                child_state = problem.result(node.state, action)
                if child_state in explored or child_state in frontier_states:
                    continue

                child = Node(
                    state=child_state,
                    parent=node,
                    action=action,
                    depth=node.depth + 1,
                    path_cost=node.path_cost + _step_cost(problem, node.state, child_state),
                )
                frontier.append(child)
                frontier_states.add(child_state)

        return SearchResult(
            None,
            problem,
            expanded_nodes,
            max_frontier_size,
            expansion_order,
            time.perf_counter() - start_time,
        )
