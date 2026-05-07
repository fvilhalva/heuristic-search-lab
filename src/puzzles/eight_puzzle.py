"""Implementation of the 8-puzzle problem."""

from typing import Tuple, List


class EightPuzzle:
    """8-puzzle problem: arrange numbers 1-8 with one empty space (0)."""

    def __init__(
        self, initial_state: Tuple[int, ...], goal_state: Tuple[int, ...] = None
    ):
        self.initial_state = initial_state
        self.goal_state = goal_state or (0, 1, 2, 3, 4, 5, 6, 7, 8)

    def actions(self, state: Tuple[int, ...]) -> List[str]:
        """Return valid actions (moves) for a given state.

        Actions: 'up', 'down', 'left', 'right' - directions to move the empty tile.
        """
        state_list = list(state)
        blank_pos = state_list.index(0)
        row, col = blank_pos // 3, blank_pos % 3
        valid_actions = []

        # Check if blank can move up (if not in top row)
        if row > 0:
            valid_actions.append("up")
        # Check if blank can move down (if not in bottom row)
        if row < 2:
            valid_actions.append("down")
        # Check if blank can move left (if not in first column)
        if col > 0:
            valid_actions.append("left")
        # Check if blank can move right (if not in last column)
        if col < 2:
            valid_actions.append("right")

        return valid_actions

    def result(self, state: Tuple[int, ...], action: str) -> Tuple[int, ...]:
        """Return the resulting state after applying an action."""
        state_list = list(state)
        blank_pos = state_list.index(0)
        row, col = blank_pos // 3, blank_pos % 3

        # Determine new position based on action
        if action == "up":
            new_pos = (row - 1) * 3 + col
        elif action == "down":
            new_pos = (row + 1) * 3 + col
        elif action == "left":
            new_pos = row * 3 + (col - 1)
        elif action == "right":
            new_pos = row * 3 + (col + 1)
        else:
            raise ValueError(f"Invalid action: {action}")

        # Swap blank with target position
        state_list[blank_pos], state_list[new_pos] = (
            state_list[new_pos],
            state_list[blank_pos],
        )
        return tuple(state_list)

    def goal_test(self, state: Tuple[int, ...]) -> bool:
        """Test if state is the goal state."""
        return state == self.goal_state

    def heuristic(self, state: Tuple[int, ...]) -> float:
        """Manhattan distance heuristic."""
        distance = 0
        for i, value in enumerate(state):
            if value != 0:
                goal_pos = self.goal_state.index(value)
                current_row, current_col = i // 3, i % 3
                goal_row, goal_col = goal_pos // 3, goal_pos % 3
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance
