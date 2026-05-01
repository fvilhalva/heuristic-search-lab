"""Template for the 8-puzzle problem."""


class EightPuzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def actions(self, state):
        raise NotImplementedError("Define valid actions for the 8-puzzle here.")

    def result(self, state, action):
        raise NotImplementedError("Define state transitions for the 8-puzzle here.")

    def goal_test(self, state):
        raise NotImplementedError("Define the goal test for the 8-puzzle here.")

    def heuristic(self, state):
        raise NotImplementedError("Define a heuristic for the 8-puzzle here.")
