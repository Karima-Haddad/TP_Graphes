"""
Service MST — couche métier entre les routes et les algorithmes.
Convertit les modèles Pydantic en dicts purs pour les algorithmes,
puis retourne le résultat brut (dict).
"""

from backend.algorithms.kruskal import run_kruskal
from backend.algorithms.prim import run_prim


def execute_mst(algorithm: str, graph_dict: dict, params: dict) -> dict:
    """
    Dispatche vers l'algorithme demandé et retourne le résultat.

    :param algorithm: "prim" | "kruskal"
    :param graph_dict: graphe sérialisé en dict pur
    :param params: paramètres propres à l'algorithme
    :returns: dict conforme au contrat GraphLab
    """
    algorithm = algorithm.lower().strip()

    if algorithm == "kruskal":
        return run_kruskal(graph_dict, params)
    elif algorithm == "prim":
        return run_prim(graph_dict, params)
    else:
        return {
            "success": False,
            "algorithm": algorithm,
            "message": f"Algorithme '{algorithm}' non reconnu dans ce service.",
            "params": params,
            "result": None,
            "visualization": None,
            "meta": {"execution_time_ms": 0, "step_count": 0, "warnings": []},
            "error": {
                "code": "INVALID_PARAMS",
                "type": "validation_error",
                "field": "algorithm",
                "details": {"received": algorithm, "expected": ["prim", "kruskal"]},
            },
        }