"""
utils.py — Fonctions utilitaires partagées entre tous les algorithmes.
Gère la reconstruction de chemin et la construction des réponses JSON du contrat.
"""

import time
from typing import Optional

try:
    from backend.models.models import Graph
except ModuleNotFoundError:  # pragma: no cover - compatibilite uvicorn depuis backend/
    from models.models import Graph


# ─────────────────────────────────────────────
# Reconstruction du chemin depuis les prédécesseurs
# ─────────────────────────────────────────────

def reconstruct_path(predecessors: dict, source: str, target: str) -> list[str]:
    """
    Remonte le dictionnaire des prédécesseurs pour construire le chemin source → target.
    Retourne [] si aucun chemin n'existe.
    """
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = predecessors.get(current)
        # Sécurité : boucle infinie impossible si predecessors est cohérent
        if current == target:
            break

    path.reverse()

    # Le chemin est valide seulement s'il commence par la source
    if path and path[0] == source:
        return path
    return []


def get_path_edges(graph: Graph, path: list[str]) -> list[str]:
    """
    À partir d'un chemin (liste de nœuds), retourne les ids des arêtes empruntées.
    """
    edge_ids = []
    for i in range(len(path) - 1):
        src, tgt = path[i], path[i + 1]
        for edge in graph.edges.values():
            if edge.source == src and edge.target == tgt:
                edge_ids.append(edge.id)
                break
            elif not graph.directed and edge.source == tgt and edge.target == src:
                edge_ids.append(edge.id)
                break
    return edge_ids


# ─────────────────────────────────────────────
# Construction des réponses du contrat
# ─────────────────────────────────────────────

def build_success_response(
    algorithm: str,
    params: dict,
    result: dict,
    visualization: dict,
    start_time: float,
    warnings: list = None
) -> dict:
    """Construit la réponse de succès conforme au contrat."""
    return {
        "success": True,
        "algorithm": algorithm,
        "message": "Exécution réussie",
        "params": params,
        "result": result,
        "visualization": visualization,
        "meta": {
            "execution_time_ms": round((time.time() - start_time) * 1000, 2),
            "step_count": len(visualization.get("steps", [])),
            "warnings": warnings or []
        },
        "error": None
    }


def build_error_response(
    algorithm: str,
    params: dict,
    message: str,
    code: str,
    error_type: str = "validation_error",
    field: str = None,
    details: dict = None
) -> dict:
    """Construit la réponse d'erreur conforme au contrat."""
    return {
        "success": False,
        "algorithm": algorithm,
        "message": message,
        "params": params,
        "result": None,
        "visualization": None,
        "meta": {
            "execution_time_ms": 0,
            "step_count": 0,
            "warnings": []
        },
        "error": {
            "code": code,
            "type": error_type,
            "field": field,
            "details": details or {}
        }
    }


# ─────────────────────────────────────────────
# Construction des étapes de visualisation
# ─────────────────────────────────────────────

def make_step(
    index: int,
    title: str,
    description: str,
    highlighted_nodes: list = None,
    highlighted_edges: list = None,
    visited_nodes: list = None,
    selected_nodes: list = None,
    selected_edges: list = None,
    node_labels: dict = None,
    edge_labels: dict = None,
    node_colors: dict = None,
    edge_colors: dict = None,
    extra: dict = None
) -> dict:
    """Construit un objet étape conforme au format du contrat."""
    return {
        "index": index,
        "title": title,
        "description": description,
        "state": {
            "highlighted_nodes": highlighted_nodes or [],
            "highlighted_edges": highlighted_edges or [],
            "visited_nodes": visited_nodes or [],
            "selected_nodes": selected_nodes or [],
            "selected_edges": selected_edges or [],
            "node_labels": node_labels or {},
            "edge_labels": edge_labels or {},
            "node_colors": node_colors or {},
            "edge_colors": edge_colors or {},
            "extra": extra or {}
        }
    }


def format_distances_as_labels(distances: dict) -> dict:
    """Convertit le dictionnaire de distances en labels affichables (∞ pour infini)."""
    INF = float('inf')
    return {
        node: ("∞" if dist == INF else str(dist))
        for node, dist in distances.items()
    }
