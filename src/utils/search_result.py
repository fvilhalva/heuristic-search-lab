"""Search result data structure used by all algorithms."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

from src.utils.node import Node


@dataclass
class SearchResult:
    """Stores the output of a search execution."""

    node: Optional[Node]
    problem: Any
    expanded_nodes: int = 0
    frontier_max_size: int = 0
    expansion_order: List[Any] = field(default_factory=list)
    elapsed_time: float = 0.0

    @property
    def path(self) -> List[Node]:
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
        """Return the total path cost of the solution."""
        return self.node.path_cost if self.node else 0.0
