"""Implementation of the Romania map search problem."""

from __future__ import annotations

from typing import Dict, List, Tuple


class RomaniaMap:
    """Romania map with cities and road distances for pathfinding problems."""

    GRAPH: Dict[str, List[Tuple[str, int]]] = {
        "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
        "Zerind": [("Arad", 75), ("Oradea", 71)],
        "Oradea": [("Zerind", 71), ("Sibiu", 151)],
        "Sibiu": [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
        "Timisoara": [("Arad", 118), ("Lugoj", 111)],
        "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
        "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
        "Drobeta": [("Mehadia", 75), ("Craiova", 120)],
        "Craiova": [("Drobeta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
        "Rimnicu Vilcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
        "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
        "Pitesti": [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
        "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90), ("Urziceni", 85)],
        "Giurgiu": [("Bucharest", 90)],
        "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
        "Hirsova": [("Urziceni", 98), ("Eforie", 86)],
        "Eforie": [("Hirsova", 86)],
        "Vaslui": [("Urziceni", 142), ("Iasi", 92)],
        "Iasi": [("Vaslui", 92), ("Neamt", 87)],
        "Neamt": [("Iasi", 87)],
    }

    # Straight-line distance to Bucharest. This is the classic heuristic used in AI textbooks.
    HEURISTIC_TO_BUCHAREST: Dict[str, int] = {
        "Arad": 366,
        "Bucharest": 0,
        "Craiova": 160,
        "Drobeta": 242,
        "Eforie": 161,
        "Fagaras": 176,
        "Giurgiu": 77,
        "Hirsova": 151,
        "Iasi": 226,
        "Lugoj": 244,
        "Mehadia": 241,
        "Neamt": 234,
        "Oradea": 380,
        "Pitesti": 100,
        "Rimnicu Vilcea": 193,
        "Sibiu": 253,
        "Timisoara": 329,
        "Urziceni": 80,
        "Vaslui": 199,
        "Zerind": 374,
    }

    def __init__(self, initial_city: str, goal_city: str = "Bucharest"):
        initial_city = self.normalize_city(initial_city)
        goal_city = self.normalize_city(goal_city)

        if initial_city not in self.GRAPH:
            raise ValueError(f"Cidade inicial inválida: {initial_city}")
        if goal_city not in self.GRAPH:
            raise ValueError(f"Cidade objetivo inválida: {goal_city}")

        self.initial_city = initial_city
        self.initial_state = initial_city
        self.goal_city = goal_city

    @classmethod
    def cities(cls) -> List[str]:
        """Return all city names sorted alphabetically."""
        return sorted(cls.GRAPH.keys())

    @classmethod
    def normalize_city(cls, city: str) -> str:
        """Normalize a user-typed city name to the canonical map name."""
        city = city.strip()
        if city in cls.GRAPH:
            return city

        normalized = city.lower().replace("-", " ").replace("_", " ")
        normalized = " ".join(normalized.split())
        aliases = {
            "bucareste": "Bucharest",
            "bucharest": "Bucharest",
            "rimnicu vilcea": "Rimnicu Vilcea",
            "râmnicu vilcea": "Rimnicu Vilcea",
            "ramnicu vilcea": "Rimnicu Vilcea",
            "iasi": "Iasi",
            "iași": "Iasi",
        }
        if normalized in aliases:
            return aliases[normalized]

        for canonical in cls.GRAPH:
            if canonical.lower() == normalized:
                return canonical
        return city

    def actions(self, city: str) -> List[str]:
        """Return available neighboring cities from a given city."""
        return [neighbor for neighbor, _ in self.GRAPH.get(city, [])]

    def result(self, city: str, action: str) -> str:
        """Return the city reached by taking a route from the current city."""
        if action in self.actions(city):
            return action
        raise ValueError(f"Não é possível ir de {city} para {action}")

    def goal_test(self, city: str) -> bool:
        """Test if the current city is the goal city."""
        return city == self.goal_city

    def heuristic(self, city: str) -> float:
        """Return h(n), the straight-line distance heuristic.

        The built-in table is only for Bucharest. If the goal is not Bucharest, the
        heuristic returns 0 so A* behaves like Uniform-Cost Search. This keeps the
        program correct for arbitrary goals typed by the teacher.
        """
        if self.goal_city != "Bucharest":
            return 0.0
        return float(self.HEURISTIC_TO_BUCHAREST.get(city, 0))

    def get_distance(self, city1: str, city2: str) -> float:
        """Get the road distance between two neighboring cities."""
        for neighbor, distance in self.GRAPH.get(city1, []):
            if neighbor == city2:
                return float(distance)
        raise ValueError(f"Não há estrada direta entre {city1} e {city2}")
