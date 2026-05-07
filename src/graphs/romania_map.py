"""Implementation of the Romania map search problem."""

from typing import Dict, List, Tuple


class RomaniaMap:
    """Romania map with cities and distances for pathfinding problems."""

    # Graph: {city: [(neighbor, distance), ...]}
    GRAPH = {
        "Oradea": [("Neamt", 71), ("Zerind", 71)],
        "Zerind": [("Oradea", 71), ("Sibiu", 151), ("Arad", 140)],
        "Arad": [("Zerind", 140), ("Sibiu", 140), ("Timisoara", 118)],
        "Timisoara": [("Arad", 118), ("Lugoj", 111)],
        "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
        "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
        "Drobeta": [("Mehadia", 75)],
        "Sibiu": [
            ("Arad", 140),
            ("Zerind", 151),
            ("Rimnicu Vilcea", 80),
            ("Craiova", 138),
        ],
        "Rimnicu Vilcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
        "Craiova": [("Sibiu", 138), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
        "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
        "Pitesti": [("Rimnicu Vilcea", 97), ("Bucharest", 101), ("Craiova", 138)],
        "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90)],
        "Giurgiu": [("Bucharest", 90)],
        "Neamt": [("Oradea", 71), ("Iasi", 87)],
        "Iasi": [("Neamt", 87), ("Vaslui", 92)],
        "Vaslui": [("Iasi", 92), ("Urziceni", 142)],
        "Urziceni": [("Vaslui", 142), ("Bucharest", 85)],
    }

    # Straight-line distance to Bucharest (heuristic)
    HEURISTIC_DISTANCES = {
        "Oradea": 380,
        "Zerind": 374,
        "Arad": 366,
        "Timisoara": 329,
        "Lugoj": 244,
        "Mehadia": 241,
        "Drobeta": 242,
        "Sibiu": 253,
        "Rimnicu Vilcea": 193,
        "Craiova": 160,
        "Fagaras": 176,
        "Pitesti": 100,
        "Bucharest": 0,
        "Giurgiu": 77,
        "Neamt": 234,
        "Iasi": 226,
        "Vaslui": 199,
        "Urziceni": 80,
    }

    def __init__(self, initial_city: str, goal_city: str = "Bucharest"):
        self.initial_city = initial_city
        self.initial_state = initial_city  # For compatibility with search algorithms
        self.goal_city = goal_city

    def actions(self, city: str) -> List[str]:
        """Return available neighboring cities from a given city."""
        return [neighbor for neighbor, distance in self.GRAPH.get(city, [])]

    def result(self, city: str, action: str) -> str:
        """Return the city reached by taking a route from current city."""
        # action is the neighbor city name
        if action in self.actions(city):
            return action
        else:
            raise ValueError(f"Cannot move from {city} to {action}")

    def goal_test(self, city: str) -> bool:
        """Test if we reached the goal city."""
        return city == self.goal_city

    def heuristic(self, city: str) -> float:
        """Straight-line distance to Bucharest heuristic."""
        return self.HEURISTIC_DISTANCES.get(city, float("inf"))

    def get_distance(self, city1: str, city2: str) -> float:
        """Get the distance between two cities."""
        for neighbor, distance in self.GRAPH.get(city1, []):
            if neighbor == city2:
                return distance
        return float("inf")
