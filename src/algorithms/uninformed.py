"""Implementation of uninformed search algorithms."""

from collections import deque
from typing import Optional, Tuple, List
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


class BFS:
    """Breadth-First Search - expands nodes level by level."""

    def solve(self, problem) -> SearchResult:
        """Find solution using BFS."""
        start = Node(state=problem.initial_state, depth=0, path_cost=0)

        if problem.goal_test(start.state):
            return SearchResult(start, problem, expanded_nodes=0)

        frontier = deque([start])
        explored = set()
        expanded_nodes = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.popleft()

            if problem.goal_test(node.state):
                return SearchResult(node, problem, expanded_nodes, max_frontier_size)

            explored.add(node.state)
            expanded_nodes += 1

            for action in problem.actions(node.state):
                child_state = problem.result(node.state, action)

                if child_state not in explored and child_state not in [
                    n.state for n in frontier
                ]:
                    child = Node(
                        state=child_state,
                        parent=node,
                        action=action,
                        depth=node.depth + 1,
                        path_cost=node.path_cost + 1,
                    )
                    frontier.append(child)

        return SearchResult(None, problem, expanded_nodes, max_frontier_size)


class DFS:
    """Depth-First Search - expands nodes in depth first manner."""

    def solve(self, problem) -> SearchResult:
        """Find solution using DFS."""
        start = Node(state=problem.initial_state, depth=0, path_cost=0)

        if problem.goal_test(start.state):
            return SearchResult(start, problem, expanded_nodes=0)

        frontier = [start]
        explored = set()
        expanded_nodes = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.pop()  # DFS: pop from end (LIFO)

            if problem.goal_test(node.state):
                return SearchResult(node, problem, expanded_nodes, max_frontier_size)

            explored.add(node.state)
            expanded_nodes += 1

            for action in reversed(
                problem.actions(node.state)
            ):  # Reverse to maintain order
                child_state = problem.result(node.state, action)

                if child_state not in explored and child_state not in [
                    n.state for n in frontier
                ]:
                    child = Node(
                        state=child_state,
                        parent=node,
                        action=action,
                        depth=node.depth + 1,
                        path_cost=node.path_cost + 1,
                    )
                    frontier.append(child)

        return SearchResult(None, problem, expanded_nodes, max_frontier_size)
