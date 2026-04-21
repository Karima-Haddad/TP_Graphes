"""Modeles de donnees lies a la representation d'un graphe."""


class Graph:
    """Structure minimale de graphe a faire evoluer selon les besoins."""

    def __init__(self, nodes=None, edges=None, directed=False, weighted=False):
        self.nodes = nodes or []
        self.edges = edges or []
        self.directed = directed
        self.weighted = weighted
