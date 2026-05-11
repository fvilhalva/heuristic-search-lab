"""Implementation of the 8-puzzle problem."""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

State = Tuple[int, ...]


class EightPuzzle:
    """8-puzzle problem: arrange numbers 1-8 with one empty space represented by 0."""

    VALID_TILES = set(range(9))

    def __init__(
        self,
        initial_state: State,
        goal_state: State | None = None,
        heuristic_name: str = "manhattan",
    ):
        self.initial_state = tuple(initial_state)
        self.goal_state = tuple(goal_state or (1, 2, 3, 4, 5, 6, 7, 8, 0))
        self.heuristic_name = heuristic_name

        self.validate_state(self.initial_state)
        self.validate_state(self.goal_state)

        self._goal_positions: Dict[int, int] = {
            value: index for index, value in enumerate(self.goal_state)
        }

    @classmethod
    def validate_state(cls, state: Iterable[int]) -> None:
        """Validate that the state contains exactly the numbers 0 through 8."""
        state_tuple = tuple(state)
        if len(state_tuple) != 9:
            raise ValueError("O estado do 8-puzzle deve ter exatamente 9 números.")
        if set(state_tuple) != cls.VALID_TILES:
            raise ValueError("O estado deve conter os números de 0 a 8, sem repetição.")

    @staticmethod
    def inversion_count(state: State) -> int:
        """Count inversions, ignoring the blank tile 0."""
        values = [value for value in state if value != 0]
        inversions = 0
        for i in range(len(values)):
            for j in range(i + 1, len(values)):
                if values[i] > values[j]:
                    inversions += 1
        return inversions

    @classmethod
    def is_solvable_pair(cls, initial_state: State, goal_state: State) -> bool:
        """Return True if initial_state can reach goal_state in a 3x3 puzzle."""
        cls.validate_state(initial_state)
        cls.validate_state(goal_state)
        return cls.inversion_count(initial_state) % 2 == cls.inversion_count(goal_state) % 2

    def is_solvable(self) -> bool:
        """Return True if the configured puzzle instance is solvable."""
        return self.is_solvable_pair(self.initial_state, self.goal_state)

    def actions(self, state: State) -> List[str]:
        """Return valid actions for the blank tile.

        Actions are the directions to move the blank tile: up, down, left, right.
        """
        blank_pos = state.index(0)
        row, col = blank_pos // 3, blank_pos % 3
        valid_actions = []

        if row > 0:
            valid_actions.append("up")
        if row < 2:
            valid_actions.append("down")
        if col > 0:
            valid_actions.append("left")
        if col < 2:
            valid_actions.append("right")

        return valid_actions

    def result(self, state: State, action: str) -> State:
        """Return the resulting state after applying an action."""
        state_list = list(state)
        blank_pos = state_list.index(0)
        row, col = blank_pos // 3, blank_pos % 3

        if action == "up" and row > 0:
            new_pos = (row - 1) * 3 + col
        elif action == "down" and row < 2:
            new_pos = (row + 1) * 3 + col
        elif action == "left" and col > 0:
            new_pos = row * 3 + (col - 1)
        elif action == "right" and col < 2:
            new_pos = row * 3 + (col + 1)
        else:
            raise ValueError(f"Movimento inválido para este estado: {action}")

        state_list[blank_pos], state_list[new_pos] = state_list[new_pos], state_list[blank_pos]
        return tuple(state_list)

    def goal_test(self, state: State) -> bool:
        """Test if state is the goal state."""
        return state == self.goal_state

    def step_cost(self, state: State, next_state: State) -> float:
        """Every valid movement in the 8-puzzle has cost 1."""
        return 1.0

    def heuristic(self, state: State) -> float:
        """Return the configured heuristic value for a state."""
        if self.heuristic_name == "misplaced":
            return float(self.misplaced_tiles(state))
        if self.heuristic_name == "manhattan":
            return float(self.manhattan_distance(state))
        if self.heuristic_name == "zero":
            return 0.0
        raise ValueError(f"Heurística inválida: {self.heuristic_name}")

    def misplaced_tiles(self, state: State) -> int:
        """h1: count tiles that are not in their goal position, ignoring 0."""
        return sum(
            1
            for index, value in enumerate(state)
            if value != 0 and value != self.goal_state[index]
        )

    def manhattan_distance(self, state: State) -> int:
        """h2: sum Manhattan distances from each tile to its goal position."""
        distance = 0
        for current_index, value in enumerate(state):
            if value == 0:
                continue
            goal_index = self._goal_positions[value]
            current_row, current_col = divmod(current_index, 3)
            goal_row, goal_col = divmod(goal_index, 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance
