"""Template for search nodes."""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Node:
    state: Any
    parent: Optional["Node"] = None
    action: Optional[Any] = None
    path_cost: float = 0.0
    depth: int = 0
    priority: float = field(default=0.0, compare=False)

    def path(self):
        raise NotImplementedError("Implement path reconstruction here.")
