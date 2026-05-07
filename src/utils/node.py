"""Template for search nodes."""

from dataclasses import dataclass, field
from typing import Any, Optional, List


@dataclass
class Node:
    state: Any
    parent: Optional["Node"] = None
    action: Optional[Any] = None
    path_cost: float = 0.0
    depth: int = 0
    priority: float = field(default=0.0, compare=False)

    def path(self) -> List["Node"]:
        """Reconstruct the path from root to this node."""
        node = self
        path = []
        while node is not None:
            path.append(node)
            node = node.parent
        return path[::-1]

    def __lt__(self, other: "Node") -> bool:
        """Compare nodes by priority (for priority queue)."""
        return self.priority < other.priority
