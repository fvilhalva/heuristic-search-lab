"""Template for the Romania map search problem."""


class RomaniaMap:
    def __init__(self, initial_city, goal_city):
        self.initial_city = initial_city
        self.goal_city = goal_city

    def actions(self, city):
        raise NotImplementedError("Define available routes here.")

    def result(self, city, action):
        raise NotImplementedError("Define route transitions here.")

    def goal_test(self, city):
        raise NotImplementedError("Define the goal test here.")

    def heuristic(self, city):
        raise NotImplementedError("Define a heuristic for the map here.")
