"""
models.py — Structures de données communes pour tous les algorithmes.
Représente un graphe à partir du format JSON du contrat.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:
    id: str
    label: str
    x: float = 0.0
    y: float = 0.0
    data: dict = field(default_factory=dict)


@dataclass
class Edge:
    id: str
    source: str
    target: str
    weight: float = 1.0
    label: str = ""
    data: dict = field(default_factory=dict)


class Graph:
    """
    Représentation d'un graphe à partir du JSON du contrat.
    Fournit des méthodes utilitaires pour accéder aux voisins et aux arêtes.
    """

    def __init__(self, graph_data: dict):
        self.directed: bool = graph_data.get("directed", False)
        self.weighted: bool = graph_data.get("weighted", True)

        # Dictionnaires indexés par id pour un accès rapide
        self.nodes: dict[str, Node] = {}
        self.edges: dict[str, Edge] = {}

        for n in graph_data.get("nodes", []):
            self.nodes[n["id"]] = Node(
                id=n["id"],
                label=n.get("label", n["id"]),
                x=n.get("x", 0.0),
                y=n.get("y", 0.0),
                data=n.get("data", {})
            )

        for e in graph_data.get("edges", []):
            self.edges[e["id"]] = Edge(
                id=e["id"],
                source=e["source"],
                target=e["target"],
                weight=e.get("weight", 1.0),
                label=e.get("label", ""),
                data=e.get("data", {})
            )

    def get_neighbors(self, node_id: str) -> list[tuple[str, float, str]]:
        """
        Retourne les voisins accessibles depuis node_id.
        Chaque élément : (node_cible, poids, edge_id)
        Pour un graphe non orienté, les deux sens sont considérés.
        """
        neighbors = []
        for edge in self.edges.values():
            if edge.source == node_id:
                neighbors.append((edge.target, edge.weight, edge.id))
            elif not self.directed and edge.target == node_id:
                neighbors.append((edge.source, edge.weight, edge.id))
        return neighbors

    def get_predecessors(self, node_id: str) -> list[tuple[str, float, str]]:
        """
        Retourne les prédécesseurs d'un nœud (utile pour Bellman sur DAG).
        Chaque élément : (node_source, poids, edge_id)
        """
        predecessors = []
        for edge in self.edges.values():
            if edge.target == node_id:
                predecessors.append((edge.source, edge.weight, edge.id))
            elif not self.directed and edge.source == node_id:
                predecessors.append((edge.target, edge.weight, edge.id))
        return predecessors

    def has_negative_weights(self) -> bool:
        """Vérifie si le graphe contient au moins un poids négatif."""
        return any(e.weight < 0 for e in self.edges.values())

    def validate_node(self, node_id: str) -> bool:
        """Vérifie qu'un nœud existe dans le graphe."""
        return node_id in self.nodes